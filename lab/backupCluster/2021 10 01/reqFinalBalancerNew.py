import cooler
import pandas as pd
from termcolor import colored
import numpy as np
import os


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


def mainfunc(inpathF, filenameF, outpathF):
    clr = cooler.Cooler(inpathF + '/' + filenameF)  # read cool file

    # find out how many valid bins in each chromosome
    A = clr.matrix(balance=True)[:, :]  # get matrix of balanced values
    A[~np.isfinite(A)] = 0  # change non-numbers to be zeros
    bins_checklist = np.sum(A, axis=0) != 0  # [ True  True  True ...  True  True False]
    nvalidDict = {}  # it will contain amounts of valid pixels for each chromosome {chromosome : count}
    bins = clr.bins()[:]
    bins = bins.groupby(['chrom']).size().reset_index(name='count') # table with format {chromosome : number of bins in it}
    #i = 0
    j = 0 # first bin of a chromosome
    chromnames_list = clr.chromnames
    for chrom in chromnames_list:
        chrom_binsize = bins.loc[bins['chrom'] == chrom, 'count'].iloc[0]
        #i += 1
        nvalid = bins_checklist[j: j + chrom_binsize].sum()
        j += chrom_binsize
        nvalidDict[chrom] = nvalid

    mtx = clr.matrix(balance=True, as_pixels=True, join=True)[:, :]
    mtx['balanced'] = mtx['balanced'].fillna(value=0)  # change non-numbers to be zeros
    mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', 'count'])  # remove these columns
    trans_contacts = mtx[mtx['chrom1'] != mtx['chrom2']]  # select trans contacts
    mtx = trans_contacts.groupby(by=['chrom1', 'chrom2']).sum()  # merge all contacts for a given pair of chromosomes

    # trick to get correct table form
    mtx.to_csv(filenameF + '.csv')
    mtx = pd.read_csv(filenameF + '.csv')
    os.remove(filenameF + '.csv')

    mtx = mtx[mtx['balanced'].notna()]  # keep only rows where contacts are numbers
    mtx = mtx.reset_index(drop=True)  # resets indexes

    mtx['balanced'] = mtx['balanced'].div(mtx['balanced'].sum())  # normalize by total trans sum

    for idx in mtx.index:  # apply valid size normalization
        mtx['balanced'][idx] = mtx['balanced'][idx] / (
                nvalidDict[mtx['chrom1'][idx]] * nvalidDict[mtx['chrom2'][idx]])

    mtx.to_csv(outpathF + '/contacts_of_specimen_' + key(filenameF) + '.csv', index=False, index_label=False)


inpath = '/mnt/storage/home/knostroverkhii/workspace/input'
outpath = '/mnt/storage/home/knostroverkhii/workspace/output'
filenames = os.listdir(inpath)
filenames.sort()
for filename in filenames:
    if filename.endswith('.cool'):
        mainfunc(inpath, filename, outpath)
        print(colored("frame is constructed", 'blue'))
print(colored("script finished", 'green'))
