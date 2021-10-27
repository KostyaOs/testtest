import cooler
import sys
import pandas as pd
from termcolor import colored
import numpy as np
import os
from collections import Counter


def frame(cool_file):
    # read cool file
    clr = cooler.Cooler(cool_file)

    # check for presence of Y chromosome
    chromnames_list = clr.chromnames

    # find out how many valid bins in each chromosome
    A = clr.matrix(balance=True)[:, :]  # get matrix of balanced values
    A[~np.isfinite(A)] = 0  # change non-numbers to be zeros
    bins_checklist = np.sum(A, axis=0) != 0  # [ True  True  True ...  True  True False]
    nvalidDict = {}  # it will contain amounts of valid pixels for each chromosome {chromosome : count}
    bins = clr.bins()[:]
    bins = bins.groupby(['chrom']).size().reset_index(name='count')
    i = 0
    j = 0
    for chrom in chromnames_list:
        chrom_binsize = bins.loc[bins['chrom'] == chrom, 'count'].iloc[0]
        i += 1
        nvalid = bins_checklist[j: j + chrom_binsize].sum()
        j += chrom_binsize
        nvalidDict[chrom] = nvalid

    # calculate total amount of contacts (raw or balanced) to use as a norm
    mtx = clr.matrix(balance=True)[:]
    mtx[~np.isfinite(mtx)] = 0  # change non-numbers to be zeros
    totalContacts = mtx.sum()

    mtx = clr.matrix(balance=True, as_pixels=True, join=True)[:, :]
    mtx['balanced'] = mtx['balanced'].fillna(value=0)  # change non-numbers to be zeros
    mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', 'count'])  # remove these columns
    trans_contacts = mtx[mtx['chrom1'] != mtx['chrom2']]  # select trans contacts
    mtx = trans_contacts.groupby(by=['chrom1', 'chrom2']).sum()  # merge all contacts for a given pair of chromosomes

    mtx.to_csv(cool_file + '.csv')
    mtx = pd.read_csv(cool_file + '.csv')
    os.remove(cool_file + '.csv')

    mtx = mtx[mtx['balanced'].notna()]  # keep only rows where contacts are numbers
    mtx = mtx.reset_index(drop=True)  # resets indexes

    mtx['balanced'] = mtx['balanced'].div(totalContacts)  # apply norm to contacts

    for idx in mtx.index:  # apply normalization by nvalid and thus finally get which portion of sum of contacts from whole
        # map do contacts of a pair of valid bins (of 2 chromosomes) take
        mtx['balanced'][idx] = mtx['balanced'][idx] / (
                nvalidDict[mtx['chrom1'][idx]] * nvalidDict[mtx['chrom2'][idx]])

    print(colored("frame is constructed", 'blue'))

    return mtx


def key(fileF):
    return fileF[:fileF.find('.cool')]


# returns pathology of specimen
def pathology(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'pathology'].iloc[0]


# returns sex of specimen
def sex(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'sex'].iloc[0]


# returns celltype of specimen
def celltype(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'cellType'].iloc[0]


# returns amount of chromosomes of specimen
def chromamount(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'amountOfChromosomes'].iloc[0]


# returns set of gonosomes of specimen
def gonosomes(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'sexChromosomes'].iloc[0]

input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
specimenInfo = pd.read_csv('specimenInfo.csv')    # open specimen info



# select threshold
threshold = 4.081417514160806

# calculate outliers
norm = 'ARC2.cool'
a = frame(input_path + '/' + norm)
case = 'HF-18-Y.cool'
b = frame(input_path + '/' + case)

# get differences
result = (a['balanced'] - b['balanced']) / ((a['balanced'] + b['balanced']) / 2)
result.to_csv('check.csv')

print(colored("FINISHED FOR ONE GROUP", 'green'))

