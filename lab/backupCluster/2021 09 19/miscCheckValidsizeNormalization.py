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
    nvalidDict = {}  # it will contain amounts of valid pixels for each chromosome
    bins = clr.bins()[:]
    #print(bins)
    totalbins = len(bins.index)
    bins = bins.groupby(['chrom']).size().reset_index(name='count')
    #print(bins)
    #print('count sum is ' + str(bins['count'].sum()))
    #print('it should be ' + str(totalbins))
    i = 0
    j = 0
    for chrom in chromnames_list:
        chrom_binsize = bins.loc[bins['chrom'] == chrom, 'count'].iloc[0]
        i += 1
        nvalid = bins_checklist[j: j + chrom_binsize].sum()
        j += chrom_binsize
        nvalidDict[chrom] = nvalid

    exit()



    print(colored("frame is constructed", 'yellow'))

    outputDir = '/mnt/storage/home/knostroverkhii/workspace/output'
    with open('', 'wt') as data_file:
        data_file.write('chromosome,cis,trans')
        data_file.write('\n')
        for key in dictionary.keys():
            data_file.write(f'{key},')
            data_file.write(f'{dictionary[key]["cis"]},')
            data_file.write(f'{dictionary[key]["trans"]},')
            data_file.write('\n')


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


files = os.listdir('/mnt/storage/home/knostroverkhii/workspace/input')

inputDir = '/mnt/storage/home/knostroverkhii/workspace/input'
files = os.listdir(inputDir)
for file in files:
    path = inputDir + '/' + file
    totalsum = frame(path)
