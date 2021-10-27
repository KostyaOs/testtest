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


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


specimenInfo = pd.read_csv('/mnt/storage/home/knostroverkhii/workspace/specimenInfo.csv')

norm = sys.argv[1] # may not actually be norm
case = sys.argv[2] # may not actually be case

codeNorm = key(norm)
cellTypeNorm = specimenInfo.loc[specimenInfo['code'] == codeNorm, 'cellType'].iloc[0]
amountOfChromosomesNorm = specimenInfo.loc[specimenInfo['code'] == codeNorm, 'amountOfChromosomes'].iloc[0]
sexChromosomesNorm = specimenInfo.loc[specimenInfo['code'] == codeNorm, 'sexChromosomes'].iloc[0]
sexNorm = specimenInfo.loc[specimenInfo['code'] == codeNorm, 'sex'].iloc[0]
pathologyNorm = specimenInfo.loc[specimenInfo['code'] == codeNorm, 'pathology'].iloc[0]
codeCase = key(case)
cellTypeCase = specimenInfo.loc[specimenInfo['code'] == codeCase, 'cellType'].iloc[0]
amountOfChromosomesCase = specimenInfo.loc[specimenInfo['code'] == codeCase, 'amountOfChromosomes'].iloc[0]
sexChromosomesCase = specimenInfo.loc[specimenInfo['code'] == codeCase, 'sexChromosomes'].iloc[0]
sexCase = specimenInfo.loc[specimenInfo['code'] == codeCase, 'sex'].iloc[0]
pathologyCase = specimenInfo.loc[specimenInfo['code'] == codeCase, 'pathology'].iloc[0]

a = frame('/mnt/storage/home/knostroverkhii/workspace/input/' + norm)
b = frame('/mnt/storage/home/knostroverkhii/workspace/input/' + case)

result = a
result['balanced'] = result['balanced'] - b['balanced']
result['balanced'] = result['balanced'] * 2
result['balanced'] = result['balanced'] / (a['balanced'] + b['balanced'])
x = result['balanced']

plt.hist(x, bins=50, range=(-5, 5))
#plt.hist(x, bins=50)

if pathologyNorm == 'none' and pathologyCase == 'none':
    title = 'N: ' + codeNorm + ' ' + cellTypeNorm + ' ' + str(
        amountOfChromosomesNorm) + ' ' + sexChromosomesNorm + ' ' + sexNorm + ' ' + pathologyNorm
    title += ' | N: ' + codeCase + ' ' + cellTypeCase + ' ' + str(
        amountOfChromosomesCase) + ' ' + sexChromosomesCase + ' ' + sexCase + ' ' + pathologyCase
    plt.gca().set(title=title, ylabel='Frequency')
    plt.savefig(
        '/mnt/storage/home/knostroverkhii/workspace/output/differences/NN,' + cellTypeNorm + ',' + sexNorm + ',' + codeNorm + ',' + codeCase + '.png')
else:
    title = 'N: ' + codeNorm + ' ' + cellTypeNorm + ' ' + str(
        amountOfChromosomesNorm) + ' ' + sexChromosomesNorm + ' ' + sexNorm + ' ' + pathologyNorm
    title += ' | C: ' + codeCase + ' ' + cellTypeCase + ' ' + str(
        amountOfChromosomesCase) + ' ' + sexChromosomesCase + ' ' + sexCase + ' ' + pathologyCase
    plt.gca().set(title=title, ylabel='Frequency')
    plt.savefig('/mnt/storage/home/knostroverkhii/workspace/output/differences/NC' + cellTypeNorm + ',' + sexNorm + ',' + codeNorm + ',' + codeCase + '.png')
