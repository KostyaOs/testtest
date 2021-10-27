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

# read cool file
cool_file = '3475-G.cool'
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

mtx.to_csv(cool_file + 'new1.csv')
mtx = pd.read_csv(cool_file + 'new1.csv')
#os.remove(cool_file + '.csv')

mtx = mtx[mtx['balanced'].notna()]  # keep only rows where contacts are numbers
mtx = mtx.reset_index(drop=True)  # resets indexes

mtx['balanced'] = mtx['balanced'].div(totalContacts)  # apply norm to contacts

for idx in mtx.index:  # apply normalization by nvalid and thus finally get which portion of sum of contacts from whole
    # map do contacts of a pair of valid bins (of 2 chromosomes) take
    mtx['balanced'][idx] = mtx['balanced'][idx] / (
            nvalidDict[mtx['chrom1'][idx]] * nvalidDict[mtx['chrom2'][idx]])

mtx.to_csv(cool_file + 'new2.csv', index = False, index_label = False)
print(colored("frame is constructed", 'yellow'))
