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
    mtx = mtx / totalContacts
    totalContacts = mtx.sum()

    return totalContacts


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


files = os.listdir('/mnt/storage/home/knostroverkhii/workspace/input')
for file in files:
    print('for specimen ' + key(file) + ' sum is ' + str(frame(file)))