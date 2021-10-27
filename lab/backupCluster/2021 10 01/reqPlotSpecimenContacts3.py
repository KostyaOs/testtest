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

inputDir = 'input'
specimenInfo = pd.read_csv('specimenInfo.csv', index_col=False)
files = os.listdir(inputDir)
for file in files:
    table = pd.read_csv(inputDir + '/' + file, index_col=False)
    labels = table['chromosome'].tolist()
    cis = table['cis'].tolist()
    trans = table['trans'].tolist()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, cis, width, label='cis')
    rects2 = ax.bar(x + width/2, trans, width, label='trans')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    code = file[:file.find('.csv')]
    cellType = specimenInfo.loc[specimenInfo['code'] == code, 'cellType'].iloc[0]
    amountOfChromosomes = specimenInfo.loc[specimenInfo['code'] == code, 'amountOfChromosomes'].iloc[0]
    sexChromosomes = specimenInfo.loc[specimenInfo['code'] == code, 'sexChromosomes'].iloc[0]
    sex = specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0]
    pathology = specimenInfo.loc[specimenInfo['code'] == code, 'pathology'].iloc[0]

    ax.set_ylabel('amount of contacts')
    ax.set_title(code + ' ' + cellType + ' ' + str(amountOfChromosomes) + ' ' + sexChromosomes + ' ' + sex + ' ' + pathology)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig('output/' + code + '.png')
    print(colored("plot has been made", 'yellow'))



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