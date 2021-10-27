import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join
import shutil

folder = 'inputnoy'
files = os.listdir(folder)
for file in files:
    # open cool file
    clr = cooler.Cooler(folder + '/' + file)
    dfb = clr.bins()[:]  # extract bins data
    dfp = clr.pixels()[:]  # extract pixels data


    select_bins = dfb  # select specified chromosome bins
    ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins


    select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] != 0]
    print(select_pixels)
    print()

    indexes = select_pixels.index.tolist()

    select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] != 0]
    print(select_pixels)

    indexes = indexes + select_pixels.index.tolist()
    indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
    print(len(indexes))


