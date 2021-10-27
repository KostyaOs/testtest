import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join


def worker(arguments):
    input_path = arguments[0]
    output_path = arguments[1]
    input_chr = arguments[2]
    numerator = int(arguments[3])
    denominator = int(arguments[4])
    multiplier = numerator / denominator

    # get source data for new cool file
    clr = cooler.Cooler(input_path)  # read cool file

    dfb = clr.bins()[:]  # extract bins data
    select_bins = dfb[dfb['chrom'] == input_chr]  # select specified chromosome bins
    ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

    dfp = clr.pixels()[:]  # extract pixels data
    if numerator < denominator:
        select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] != 1]
    else:
        select_pixels = dfp[dfp['bin1_id'].isin(ids)]
    indexes = select_pixels.index.tolist()
    if numerator < denominator:
        select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] != 1]
    else:
        select_pixels = dfp[dfp['bin2_id'].isin(ids)]
    indexes = indexes + select_pixels.index.tolist()
    indexes = list(dict.fromkeys(indexes))
    dfp.loc[indexes,'count'] *= multiplier

    cooler.create_cooler(cool_uri=output_path, bins=dfb, pixels=dfp)  # make new cool file
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
        print(colored("Current file is '" + filename + "'. Write chromosome, numerator and denominator, separated by "
                                                       "space", 'yellow'))
        arguments_list = [input_path + "/" + filename, output_path + "/" + filename] + input().split()
        list_of_lists.append(arguments_list)

for arguments_list in list_of_lists:
    worker(arguments_list)

print(colored("SCV: 'Job finished!'", 'green'))