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


specimenInfo = pd.read_csv('specimenInfo.csv')

cools = os.listdir('/mnt/storage/home/knostroverkhii/workspace/input')

ChorionFemale = []
FibroblastFemale = []
Male = []

groups = [ChorionFemale, FibroblastFemale, Male]
for file in cools:
    code = key(file)
    if specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0] == 'female':
        if specimenInfo.loc[specimenInfo['code'] == code, 'cellType'].iloc[0] == 'chorion':
            ChorionFemale.append(file)
        elif specimenInfo.loc[specimenInfo['code'] == code, 'cellType'].iloc[0] == 'fibroblast':
            FibroblastFemale.append(file)
    elif specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0] == 'male':
        Male.append(file)


if not os.path.exists('/mnt/storage/home/knostroverkhii/workspace/output/differences'):
    os.mkdir('/mnt/storage/home/knostroverkhii/workspace/output/differences')

for group in groups:
    groupCopy = group.copy()
    for file1 in group:
        code = key(file1)
        if specimenInfo.loc[specimenInfo['code'] == code, 'pathology'].iloc[0] == 'none':
            for file2 in groupCopy:
                if file1 != file2:
                    command = 'echo "source /mnt/storage/home/knostroverkhii/anaconda3/envs/fromAlina/bin/activate; python workspace/reqPlotDifferences2.py ' + file1 + ' ' + file2 + '" | qsub -l select=1:ncpus=1:mem=6gb,walltime=0:20:0'
                    os.system(command)
            groupCopy.remove(file1)