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

# select only '.cool' files
contents = os.listdir(input_path)
filenames = []
for i in contents:
    if i.endswith('.cool'):
        filenames.append(i)

specimenInfo = pd.read_csv('specimenInfo.csv')    # open specimen info
thresholds = pd.read_csv('thresholds.csv')  # open thresholds table

# make lists, each filled with files of specimens of specific group
ChorionFemale = []
FibroblastFemale = []
Male = []
groups = [ChorionFemale, FibroblastFemale, Male]
for filename in filenames:
    code = key(filename)
    if sex(code) == 'female':
        if celltype(code) == 'chorion':
            ChorionFemale.append(filename)
        elif celltype(code) == 'fibroblast':
            FibroblastFemale.append(filename)
    elif sex(code) == 'male':
        Male.append(filename)

counter = 0 # counter for threshold selection
for group in groups:
    # make lists of files of norms and files of cases
    norms = []
    cases = []
    for filename in group:
        code = key(filename)
        if pathology(code) == 'none':
            norms.append(filename)
        else:
            cases.append(filename)

    # make dictionary to be filled and turned into .csv
    dictionary = {}
    for case in cases:
        code = key(case)
        dictionary[code] = {
            'specimenInfo': [code, celltype(code), sex(code), chromamount(code), gonosomes(code), pathology(code)],
            'norm': [],
            'threshold': [],
            'amount of outliers': [],
            '1st chr': [],
            '2nd chr': [],
            '3rd chr': [],
        }

    # select threshold
    threshold = thresholds['threshold'][counter]

    # calculate outliers
    for norm in norms:
        codeNorm = key(norm)
        a = frame(input_path + '/' + norm)
        for case in cases:
            code = key(case)
            dictionary[code]['norm'].append(codeNorm)  # send to dictionary
            dictionary[code]['threshold'].append(threshold)  # send to dictionary

            b = frame(input_path + '/' + case)

            # get differences
            result = (a['balanced'] - b['balanced']) / ((a['balanced'] + b['balanced']) / 2)
            result.to_csv('check.csv')

            # get standard deviation (sigma)
            sigma = result.std()

            # get median and calculate distance from median for every value
            mdn = result.median()
            for idx in result.index:
                result[idx] = abs(result[idx] - mdn)

            # TODO check calculation manually. if outlierCount > 0: result.to_csv('check.csv') exit()
            # count outliers and learn most frequent outlier chromosomes and their contact count
            outlierCount = 0
            outlierChromosomes = []
            for idx in result.index:
                distance = result[idx]
                if distance > threshold * sigma:
                    outlierCount += 1
                    chrom1 = a['chrom1'][idx]
                    chrom2 = a['chrom2'][idx]
                    outlierChromosomes.append(chrom1)
                    outlierChromosomes.append(chrom2)

            # send to dictionary
            dictionary[code]['amount of outliers'].append(outlierCount)

            top3 = Counter(outlierChromosomes).most_common(3)
            denominator = len(outlierChromosomes)
            if len(top3) == 0:
                dictionary[code]['1st chr'].append('none')
                dictionary[code]['2nd chr'].append('none')
                dictionary[code]['3rd chr'].append('none')
            if len(top3) == 1:
                firstChr = str(top3[0][0]) + ', ' + str(top3[0][1] / denominator)
                print(type(firstChr))# for debug
                dictionary[code]['1st chr'].append(firstChr)
                dictionary[code]['2nd chr'].append('none')
                dictionary[code]['3rd chr'].append('none')
            if len(top3) == 2:
                firstChr = str(top3[0][0]) + ', ' + str(top3[0][1] / denominator)
                secondChr = str(top3[1][0]) + ', ' + str(top3[1][1] / denominator)
                print(type(firstChr))# for debug
                print(type(secondChr))# for debug
                dictionary[code]['1st chr'].append(firstChr)
                dictionary[code]['2nd chr'].append(secondChr)
                dictionary[code]['3rd chr'].append('none')
            if len(top3) == 3:
                firstChr = str(top3[0][0]) + ', ' + str(top3[0][1] / denominator)
                secondChr = str(top3[1][0]) + ', ' + str(top3[1][1] / denominator)
                thirdChr = str(top3[2][0]) + ', ' + str(top3[2][1] / denominator)
                print(type(firstChr))# for debug
                print(type(secondChr))# for debug
                print(type(thirdChr))# for debug
                dictionary[code]['1st chr'].append(firstChr)
                dictionary[code]['2nd chr'].append(secondChr)
                dictionary[code]['3rd chr'].append(thirdChr)

            print(colored("parameters for one combo are calculated", 'blue'))

    # write .csv for group
    print(codeNorm)
    print(sex(codeNorm))
    print(celltype(codeNorm))
    with open('output/outliers of ' + sex(codeNorm) + ' ' + celltype(codeNorm) + '.csv', 'wt') as data_file:
        for case in cases:
            for parameter in dictionary[key(case)]:
                data_file.write(f'{parameter};')
                for value in dictionary[key(case)][parameter]:
                    data_file.write(f'{value};')
                data_file.write('\n')
            data_file.write('\n')

    counter += 1
    print(colored("FINISHED FOR ONE GROUP", 'green'))

