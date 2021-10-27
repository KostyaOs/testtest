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

# SOMEWHERE detect balance coulumn

# make dictionary: {'chromosome' : Ncis, Ntrans}
# for each chromosome get Ncis and Ntrans
# make bar plot (https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html)


inputDir = sys.argv[1]
file = sys.argv[2]
clr = cooler.Cooler(inputDir + '/' + file)

# make dictionary: {'chromosome' : Ncis, Ntrans}
dictionary = {}
chrnames = clr.chromnames
for chrname in chrnames:
    dictionary[chrname] = {'cis' : 0, 'trans' : 0}

# for each chromosome get Ncis and Ntrans
mtx = pd.DataFrame(data=clr.matrix(balance=False, as_pixels=True, join=True)[:,:])
mtx['count'] = mtx['count'].fillna(value=0)

row = 0
rowsum = mtx.index[-1] + 1
for i in mtx.index:
    row += 1
    count = mtx['count'][i]
    chr1 = mtx['chrom1'][i]
    chr2 = mtx['chrom2'][i]
    if chr1 == chr2:
        dictionary[chr1]['cis'] += count
    else:
        dictionary[chr1]['trans'] += count
        dictionary[chr2]['trans'] += count
    if row % 1000000 == 0:
        print(colored(str(row) + " bin pairs out of " + str(rowsum) + " have been processed", 'yellow'))


outputDir = '/mnt/storage/home/knostroverkhii/workspace/output'
with open(outputDir + '/' + key(file) + '.csv', 'wt') as data_file:
    data_file.write('chromosome,cis,trans')
    data_file.write('\n')
    for key in dictionary.keys():
        data_file.write(f'{key},')
        data_file.write(f'{dictionary[key]["cis"]},')
        data_file.write(f'{dictionary[key]["trans"]},')
        data_file.write('\n')

choice = 0
if choice == 'make plots of differences':

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