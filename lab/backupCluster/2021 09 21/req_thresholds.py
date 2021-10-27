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

    print(colored("frame is constructed", 'yellow'))

    return mtx


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


# returns pathology of specimen
def pathology(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'pathology'].iloc[0]


# returns sex of specimen
def sex(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0]


# returns sex of specimen
def celltype(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'cellType'].iloc[0]


# check that output folder is empty
output_path = '/mnt/storage/home/knostroverkhii/workspace/output'
contents = os.listdir(output_path)  # returns list
if len(contents):
    contents.sort()
    print(colored("Output directory is not empty, below are it's contents:", 'blue'))
    for file in contents:
        print(file)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()

# show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
contents = os.listdir(input_path)  # returns list
if not len(contents):
    print(colored("Input directory is empty. Fill it if you wish to continue. Continue (Enter) or exit (Ctrl + C)?",
                  'blue'))
    input()
else:
    contents.sort()
    print(colored("Below are contents of input folder:", 'blue'))
    for file in contents:
        print(file)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()

contents = os.listdir(input_path)
filenames = []
for i in contents:
    if i.endswith('.cool'):
        filenames.append(i)
finalThresholds = []

specimenInfo = pd.read_csv('specimenInfo.csv')

ChorionFemale = []
FibroblastFemale = []
Male = []

groups = [ChorionFemale, FibroblastFemale, Male]
for filename in filenames:
    code = key(filename)
    if pathology(code) == 'none':
        if sex(code) == 'female':
            if celltype(code) == 'chorion':
                ChorionFemale.append(filename)
            elif celltype(code) == 'fibroblast':
                FibroblastFemale.append(filename)
        elif sex(code) == 'male':
            Male.append(filename)

counter = 0  # for debug
for group in groups:
    thresholds = []
    groupCopy = group.copy()
    for file1 in group:
        file1code = key(file1)
        a = frame(input_path + '/' + file1)
        for file2 in groupCopy:
            if file1 != file2:
                file2code = key(file2)
                b = frame(input_path + '/' + file2)

                print(a)
                print(b)
                if counter == 1:  # for debug
                    exit()  # for debug
                result = (a['balanced'] - b['balanced']) / ((a['balanced'] + b['balanced']) / 2)

                print(a)
                print(b)
                print(result)

                # get median and max distance from median
                # TODO check that mdn max and min are calculated based only on column
                # TODO check that on next cycle a frame is unchanged
                mdn = result.median()
                maximum = result.max()
                minimum = result.min()
                mdnMaximum = mdn - maximum
                mdnMaximum = abs(mdnMaximum)
                mdnMinimum = mdn - minimum
                mdnMinimum = abs(mdnMinimum)
                distance = max(mdnMaximum, mdnMinimum)

                # get standard deviation (sigma)
                sigma = result.std()

                print(result)
                print(mdn)
                print(maximum)
                print(minimum)

                # get threshold
                threshold = distance / sigma

                thresholds.append(threshold)
                print(colored("potential threshold is calculated, " + str(threshold), 'yellow'))
                counter += 1  # for debug


        groupCopy.remove(file1)
