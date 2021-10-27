import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join
import numpy as np


def worker(arguments):
    input_path = arguments[0][0]
    output_path = arguments[0][1]
    dictonarY = arguments[0][2]

    # open cool file
    clr = cooler.Cooler(input_path)

    # deal with gonosomes
    for keY in dictonarY.keys():
        dfb = clr.bins()[:]  # extract bins data
        select_bins = dfb[dfb['chrom'] == keY]  # select specified chromosome bins
        ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

        dfp = clr.pixels()[:]  # extract pixels data
        multiplieR = dictonarY[keY]
        if multiplieR < 1:
            select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] != 1]
        else:
            select_pixels = dfp[dfp['bin1_id'].isin(ids)]
        indexes = select_pixels.index.tolist()
        if multiplieR < 1:
            select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] != 1]
        else:
            select_pixels = dfp[dfp['bin2_id'].isin(ids)]
        indexes = indexes + select_pixels.index.tolist()
        indexes = list(dict.fromkeys(indexes))
        dfp.loc[indexes, 'count'] *= multiplieR

    # deal with autosomes
    for i in range(1, 23):
        dfb = clr.bins()[:]  # extract bins data
        select_bins = dfb[dfb['chrom'] == str(i)]  # select specified chromosome bins
        ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

        dfp = clr.pixels()[:]  # extract pixels data
        select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] != 1]
        indexes = select_pixels.index.tolist()
        select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] != 1]
        indexes = indexes + select_pixels.index.tolist()
        indexes = list(dict.fromkeys(indexes))
        dfp.loc[indexes, 'count'] *= 2 / 3

    # make new cool file
    cooler.create_cooler(cool_uri=output_path, bins=dfb, pixels=dfp)
    print(colored("file has been processed", 'blue'))


#check that output folder is empty
output_path = 'output'
contents = os.listdir(output_path) # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'yellow'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'yellow'))
    choice = input()
    if choice != 'y':
        exit()

#show what is in input (files AND directories)
input_path = 'input'
contents = os.listdir(input_path) # returns list
if not len(contents):
    print(colored("Input directory empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'yellow'))
    if choice != 'y':
        exit()
else:
    print(colored("Below are contents of input folder:", 'yellow'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'yellow'))
    choice = input()
    if choice != 'y':
        exit()

# make list of arguments
list_of_lists = []
for filename in os.listdir(input_path):
    if filename.endswith(".cool"):
        arguments_list = []
        print(colored("Current file is " + filename + "For parameters asked below use spaces as separator", 'yellow'))
        paths = [input_path + "/" + filename, output_path + "/" + filename]
        arguments_list.append(paths)
        print(colored("Type numerator and denominator for chromosomes to be multiplied", 'yellow'))
        multiplier = input().split()
        arguments_list.append(multiplier)
        print(colored("Type chromosomes to be spared", 'yellow'))
        sparedChromosomes = input().split()
        arguments_list.append(sparedChromosomes)
        list_of_lists.append(arguments_list)

for arguments_list in list_of_lists:
    worker(arguments_list)

print(colored("SCV: 'Job finished!'", 'green'))