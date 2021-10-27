import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join


def worker(arguments):
    in_path = arguments[0]
    out_path = arguments[1]

    clr = cooler.Cooler(in_path)

    dfb = clr.bins()[:]  # extract bins data
    select_bins = dfb[dfb['chrom'] == 'Y']  # select specified chromosome bins
    ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins
    dfb = dfb.drop(ids)  # delete rows with Y chromosome

    dfp = clr.pixels()[:]  # extract pixels data
    dfp = dfp.drop(dfp.loc[dfp['bin1_id'].isin(ids)].index)  # delete 1 portion of rows with Y chromosome
    dfp = dfp.drop(dfp.loc[dfp['bin2_id'].isin(ids)].index)  # delete the rest of rows with Y chromosome

    cooler.create_cooler(cool_uri=out_path, bins=dfb, pixels=dfp)  # make new cool file
    print(colored("file has been processed", 'blue'))


# check that output folder is empty
output_path = 'output'
contents = os.listdir(output_path)  # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'blue'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()

# show what is in input (files AND directories)
input_path = 'input'
contents = os.listdir(input_path)  # returns list
if not len(contents):
    print(colored("Input directory is empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'blue'))
    if choice != 'y':
        exit()
else:
    print(colored("Below are contents of input folder:", 'blue'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()

# make list of arguments
list_of_lists = []
for filename in os.listdir(input_path):
    if filename.endswith(".cool"):
        arguments_list = [input_path + "/" + filename, output_path + "/" + filename]
        list_of_lists.append(arguments_list)

for arguments_list in list_of_lists:
    worker(arguments_list)

print(colored("SCV: 'Job finished!'", 'green'))
