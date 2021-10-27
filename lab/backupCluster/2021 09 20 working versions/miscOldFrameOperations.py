import cooler
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored
import numpy as np
import math
import os
from os import listdir
from os.path import isfile, join
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
    binsize = clr.binsize
    chromsizes_list = clr.chromsizes  # two column table: first is chromosome name, second is its length is nucleotides
    nvalidDict = {}  # it will contain amounts of valid pixels for each chromosome
    i = 0
    j = 0
    for chrom in chromnames_list:
        chrom_binsize = math.ceil(chromsizes_list[i] / binsize)
        i += 1
        nvalid = bins_checklist[j: j + chrom_binsize].sum()
        j += chrom_binsize
        nvalidDict[chrom] = nvalid

    # choose value column to make map from and calculate total amount of contacts (raw or balanced) to use as a norm
    value_column = 'balanced'
    extra_column = 'count'
    mtx = clr.matrix(balance=True)[:]
    mtx[~np.isfinite(mtx)] = 0  # change non-numbers to be zeros
    totalContacts = mtx.sum()

    mtx = clr.matrix(balance=True, as_pixels=True, join=True)[:, :]
    mtx[value_column] = mtx[value_column].fillna(value=0)  # change non-numbers to be zeros
    mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', extra_column])  # remove these columns
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


choice = 0

threshold = 0.4980652484
norms = dict(norm1='ARC2.cool', norm2='PFCH6-G.cool', norm3='PFCH6-Y.cool')
cases = []

specimenInfo = pd.read_csv('specimenInfo.csv')

cases = os.listdir('input')

for norm in norms.values():
    for case in cases:
        if norm != case:
            normCode = norm[:norm.find('.cool')]
            caseCode = case[:case.find('.cool')]

            a = frame('input/' + norm)
            b = frame('input/' + case)
            result = a
            result['balanced'] = result['balanced'] - b['balanced']
            result['balanced'] = result['balanced'] * 2
            result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

            sns.set_style("white")
            dataSet = result['balanced']
            kwargs = dict(hist_kws={'alpha': .6}, kde_kws={'linewidth': 2})
            plt.figure(figsize=(10, 7), dpi=80)
            sns.distplot(dataSet, **kwargs)
            #plt.xlim(50, 75)
            #plt.legend()
            if case not in norms.values():
                plt.xlabel('Difference between norm ' + normCode + ' and case ' + caseCode)
            if case in norms.values():
                plt.xlabel('Difference between norm ' + normCode + ' and another norm ' + caseCode)
            plt.ylabel("Contacts count")
            plt.savefig('output/' + normCode + '-against-' + caseCode + '.png')
            print(colored("plot is drawn", 'yellow'))

if choice == 'make spreadsheet with only frequencies of critical contacts':
    print(colored("Type name of output spreadsheet", 'yellow'))
    outputName = input()
    threshold = 0.4980652484
    norms = dict(norm1='ARC2.cool', norm2='PFCH6-G.cool', norm3='PFCH6-Y.cool')
    cases = []

    specimenInfo = pd.read_csv('specimenInfo.csv')

    for file in os.listdir('input'):
        if file not in norms.values():
            cases.append(file)

    # leave row if difference in more than threshold
    with open('output/' + outputName + '.csv', 'wt') as data_file:
        for norm in norms.values():
            for case in cases:
                normCode = norm[:norm.find('.cool')]
                caseCode = case[:case.find('.cool')]
                amountOfChromosomes = \
                    specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'amountOfChromosomes'].iloc[0]
                sexChromosomes = \
                    specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'sexChromosomes'].iloc[
                        0]
                pathology = specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'pathology'].iloc[0]
                data_file.write('\n')
                data_file.write('norm;code;' + normCode + '\n')
                data_file.write('case;code;' + caseCode + '\n')
                data_file.write(';total amount of chromosomes;' + str(amountOfChromosomes) + '\n')
                data_file.write(';set of sex chromosomes;' + sexChromosomes + '\n')
                data_file.write(';pathology;' + pathology + '\n')
                a = frame('input/' + norm)
                b = frame('input/' + case)
                result = a
                result['balanced'] = result['balanced'] - b['balanced']
                result['balanced'] = result['balanced'] * 2
                result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

                criticalChromosomes = []
                for index in result.index:
                    difference = abs(result['balanced'][index])
                    if difference > threshold:
                        chrom1 = result['chrom1'][index]
                        chrom2 = result['chrom2'][index]
                        criticalChromosomes.append(chrom1)
                        criticalChromosomes.append(chrom2)
                data_file.write(
                    'most common critical chromosomes are;' + str(Counter(criticalChromosomes).most_common(3)) + '\n')
                data_file.write('total amount of critical chromosomes;' + str(len(criticalChromosomes)) + '\n')
                print(colored("case is written", 'yellow'))

if choice == 'make plots of differences':
    choice = 0

    norms = dict(norm1='ARC2.cool', norm2='PFCH6-G.cool', norm3='PFCH6-Y.cool')
    cases = []

    specimenInfo = pd.read_csv('specimenInfo.csv')

    for file in os.listdir('input'):
        if file not in norms.values():
            cases.append(file)

    norm = 'PFCH6-G.cool'
    case = cases[0]
    a = frame('input/' + norm)
    b = frame('input/' + case)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])
    x = result['balanced']
    plt.hist(x, bins=25)
    plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
    plt.savefig('output/plot.png')

if choice == 'get spreadsheet with critical contacts':
    print(colored("Type name of output spreadsheet", 'yellow'))
    outputName = input()
    threshold = 0.4980652484
    norms = dict(norm1='ARC2.cool', norm2='PFCH6-G.cool', norm3='PFCH6-Y.cool')
    cases = []

    specimenInfo = pd.read_csv('specimenInfo.csv')

    for file in os.listdir('input'):
        if file not in norms.values():
            cases.append(file)

    # leave row if difference in more than threshold
    with open('output/' + outputName + '.csv', 'wt') as data_file:
        for norm in norms.values():
            for case in cases:
                normCode = norm[:norm.find('.cool')]
                caseCode = case[:case.find('.cool')]
                amountOfChromosomes = \
                    specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'amountOfChromosomes'].iloc[0]
                sexChromosomes = \
                    specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'sexChromosomes'].iloc[
                        0]
                pathology = specimenInfo.loc[specimenInfo['code'] == case[:case.find('.cool')], 'pathology'].iloc[0]
                data_file.write('\n')
                data_file.write('norm code is ' + normCode + '\n')
                data_file.write('case code is ' + caseCode + '\n')
                data_file.write('case has total of ' + str(amountOfChromosomes) + ' chromosomes\n')
                data_file.write('case has following set of sex chromosomes: ' + sexChromosomes + '\n')
                data_file.write('case has following pathology: ' + pathology + '\n')
                a = frame('input/' + norm)
                b = frame('input/' + case)
                result = a
                result['balanced'] = result['balanced'] - b['balanced']
                result['balanced'] = result['balanced'] * 2
                result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

                criticalChromosomes = []
                for index in result.index:
                    difference = abs(result['balanced'][index])
                    if difference > threshold:
                        chrom1 = result['chrom1'][index]
                        chrom2 = result['chrom2'][index]
                        criticalChromosomes.append(chrom1)
                        criticalChromosomes.append(chrom2)
                        data_file.write(f'{chrom1};')
                        data_file.write(f'{chrom2};')
                        data_file.write(f'{difference};')
                        data_file.write('\n')
                data_file.write(
                    'most common chromosomes are ' + str(Counter(criticalChromosomes).most_common(3)) + '\n')
                data_file.write('total amount of critical chromosomes is ' + str(len(criticalChromosomes)) + '\n')
                print(colored("case is written", 'yellow'))

if choice == 'check threshold against maximums of aneuploidies':
    print(colored("Type name of output spreadsheet", 'yellow'))
    outputName = input()

    threshold = 0.4980652484
    norms = dict(norm1='ARC2.cool', norm2='PFCH6-G.cool', norm3='PFCH6-Y.cool')
    cases = []

    for file in os.listdir('input'):
        if file not in norms.values():
            cases.append(file)

    with open('output/' + outputName + '.csv', 'wt') as data_file:
        data_file.write('norms;')
        for norm in norms.values():
            data_file.write(f'{norm};')
        data_file.write('\n')
        for case in cases:
            data_file.write(f'{case};')
            for norm in norms.values():
                a = frame('input/' + norm)
                b = frame('input/' + case)
                result = a
                result['balanced'] = result['balanced'] - b['balanced']
                result['balanced'] = result['balanced'] * 2
                result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

                for index in result.index:
                    result['balanced'][index] = abs(result['balanced'][index])
                maxDifference = result['balanced'].max()
                DifferenceMinusThreshold = maxDifference - threshold
                data_file.write(f'{DifferenceMinusThreshold};')
                print(colored("DifferenceMinusThreshold is written", 'yellow'))
            data_file.write('\n')

if choice == 'find thresholds':
    norm1 = '3494-G.cool'
    norm2 = '3494-Y.cool'
    norm3 = '3518I.cool'
    norm4 = '3518II.cool'

    nameA = 'norm1'
    nameB = 'norm2'
    a = frame('input/' + norm1)
    b = frame('input/' + norm2)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

    nameA = 'norm1'
    nameB = 'norm3'
    a = frame('input/' + norm1)
    b = frame('input/' + norm3)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

    nameA = 'norm1'
    nameB = 'norm4'
    a = frame('input/' + norm1)
    b = frame('input/' + norm4)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

    nameA = 'norm2'
    nameB = 'norm3'
    a = frame('input/' + norm2)
    b = frame('input/' + norm3)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

    nameA = 'norm2'
    nameB = 'norm4'
    a = frame('input/' + norm2)
    b = frame('input/' + norm4)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

    nameA = 'norm3'
    nameB = 'norm4'
    a = frame('input/' + norm3)
    b = frame('input/' + norm4)
    result = a
    result['balanced'] = result['balanced'] - b['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])

    result.to_csv('output/' + nameA + '-' + nameB + '.csv')
    print(colored("file is done", 'yellow'))

if choice == 1:
    file1 = 'input/PFCH6-G.cool'
    file2 = 'input/PFCH6-Y.cool'
    file3 = 'input/ARC2.cool'

    result = frame(file1)

    result['balanced'] = result['balanced'] + frame(file2)['balanced']
    print(colored("after +", 'yellow'))
    print(result)

    result['balanced'] = result['balanced'] / 2
    print(colored("after /2", 'yellow'))
    print(result)

    result['balanced'] = result['balanced'] - frame(file3)['balanced']
    print(colored("after -", 'yellow'))
    print(result)

    result.to_csv('output/fibroblastMethodControl.csv')

    # std = result['balanced'].std()  # to calculate for specific column
    # print(colored("std", 'yellow'))
    # print(std)

if choice == 2:
    control = 'm3518I.cool'
    specimens = os.listdir('input')
    specimens.remove(control)
    for case in specimens:
        result = frame('input/' + case)

        result['balanced'] = result['balanced'] - frame('input/' + control)['balanced']

        result.to_csv('output/' + case + '.csv')
        print(colored("file is done", 'yellow'))

        # std = result['balanced'].std()  # to calculate for specific column
        # print(colored("std", 'yellow'))

if choice == 3:
    norm1 = 'ARC2.cool'
    norm2 = 'PFCH6-G.cool'
    norm3 = 'PFCH6-Y.cool'
    case = 'HF-18-G.cool'

    # norm1 - norm2
    result = frame('input/' + norm1)

    result['balanced'] = result['balanced'] - frame('input/' + norm2)['balanced']

    result.to_csv('output/norm1-norm2.csv')
    print(colored("file is done", 'yellow'))

    # norm1 - norm3
    result = frame('input/' + norm1)

    result['balanced'] = result['balanced'] - frame('input/' + norm3)['balanced']

    result.to_csv('output/norm1-norm3.csv')
    print(colored("file is done", 'yellow'))

    # norm1 - case
    result = frame('input/' + norm1)

    result['balanced'] = result['balanced'] - frame('input/' + case)['balanced']

    result.to_csv('output/norm1-case.csv')
    print(colored("file is done", 'yellow'))

    # norm2 - norm3
    result = frame('input/' + norm2)

    result['balanced'] = result['balanced'] - frame('input/' + norm3)['balanced']

    result.to_csv('output/norm2-norm3.csv')
    print(colored("file is done", 'yellow'))

    # norm2 - case
    result = frame('input/' + norm2)

    result['balanced'] = result['balanced'] - frame('input/' + case)['balanced']

    result.to_csv('output/norm2-case.csv')
    print(colored("file is done", 'yellow'))

    # norm3 - case
    result = frame('input/' + norm3)

    result['balanced'] = result['balanced'] - frame('input/' + case)['balanced']

    result.to_csv('output/norm3-case.csv')
    print(colored("file is done", 'yellow'))

if choice == 4:
    norm1 = 'ARC2.cool'
    norm2 = 'PFCH6-G.cool'
    norm3 = 'PFCH6-Y.cool'
    case = 'HF-18-G.cool'

    # norm1 - norm2
    a = norm1
    b = norm2
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))

    # norm1 - norm3
    a = norm1
    b = norm3
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))

    # norm1 - case
    a = norm1
    b = case
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))

    # norm2 - norm3
    a = norm2
    b = norm3
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))

    # norm2 - case
    a = norm2
    b = case
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))

    # norm3 - case
    a = norm3
    b = case
    result = frame('input/' + a)
    result['balanced'] = result['balanced'] - frame('input/' + b)['balanced']
    result['balanced'] = result['balanced'] * 2
    result['balanced'] = result['balanced'] / (frame('input/' + a)['balanced'] + frame('input/' + b)['balanced'])

    result.to_csv('output/' + a + '-' + b + '.csv')
    print(colored("file is done", 'yellow'))
