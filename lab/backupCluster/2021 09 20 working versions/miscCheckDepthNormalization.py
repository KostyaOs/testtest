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

    mtx = clr.matrix(balance=True)[:]
    mtx[~np.isfinite(mtx)] = 0  # change non-numbers to be zeros
    totalContacts = mtx.sum()
    mtx = mtx / totalContacts
    totalContacts = mtx.sum()

    return totalContacts


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


inputDir = '/mnt/storage/home/knostroverkhii/workspace/input'
files = os.listdir(inputDir)
for file in files:
    path = inputDir + '/' + file
    totalsum = frame(path)
    distance = abs(1 - totalsum)
    if distance < 1 - 0.99999999999999:
        print('FINE! For specimen ' + key(file) + ' sum is ' + str(totalsum))
    else:
        print('not fine? For specimen ' + key(file) + ' sum is ' + str(totalsum))
