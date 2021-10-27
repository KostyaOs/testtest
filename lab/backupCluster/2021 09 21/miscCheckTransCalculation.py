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


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


def mainfunc(inputdirF, fileF):
    clr = cooler.Cooler(inputdirF + '/' + fileF)

    mtx = pd.DataFrame(data=clr.matrix(balance=True, as_pixels=True, join=True)[:, :])
    mtx['balanced'] = mtx['balanced'].fillna(value=0)

    transtotal = 0
    row = 0
    rowsum = len(mtx.index)
    for i in mtx.index:
        row += 1
        count = mtx['balanced'][i]
        chr1 = mtx['chrom1'][i]
        chr2 = mtx['chrom2'][i]
        if chr1 != chr2:
            transtotal += count
        if row % 1000000 == 0:
            print(colored(str(row) + " bin pairs out of " + str(rowsum) + " have been processed", 'yellow'))
    print('new method gives ' + str(transtotal))

    value_column = 'balanced'
    extra_column = 'count'

    mtx = clr.matrix(balance=True, as_pixels=True, join=True)[:, :]
    mtx[value_column] = mtx[value_column].fillna(value=0)  # change non-numbers to be zeros
    mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', extra_column])  # remove these columns
    trans_contacts = mtx[mtx['chrom1'] != mtx['chrom2']]  # select trans contacts
    mtx = trans_contacts.groupby(by=['chrom1', 'chrom2']).sum()  # merge all contacts for a given pair of chromosomes

    mtx.to_csv(fileF + '.csv')
    mtx = pd.read_csv(fileF + '.csv')
    os.remove(fileF + '.csv')

    mtx = mtx[mtx['balanced'].notna()]  # keep only rows where contacts are numbers
    mtx = mtx.reset_index(drop=True)  # resets indexes

    transtotal2 = mtx['balanced'].sum()
    print('old method gives ' + str(transtotal2))

    exit()


inputdir = '/mnt/storage/home/knostroverkhii/workspace/input'
files = os.listdir(inputdir)
for file in files:
    mainfunc(inputdir, file)
