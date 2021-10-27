import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join
import numpy as np


def worker(arguments):
    in_path = arguments[0]
    out_path = arguments[1]

    clr = cooler.Cooler(in_path)

    dfb = clr.bins()[:]  # extract bins data
    dfp = clr.pixels()[:]  # extract pixels data
    dfp['count'] = dfp['count'].fillna(value=0)  # change NaN to zero
    dfp['count'] = dfp['count'] / dfp['count'].sum()  # divide contacts of each bin by all contacts

    cooler.create_cooler(cool_uri=out_path, bins=dfb, pixels=dfp)  # make new cool file
    print(colored("file has been processed", 'blue'))


#check that output folder is empty
output_path = '/mnt/storage/home/knostroverkhii/=workspace/output'
contents = os.listdir(output_path) # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'blue'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()

#show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/=workspace/input'
contents = os.listdir(input_path) # returns list
if not len(contents):
    print(colored("Directory empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'blue'))
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
input_path = '/mnt/storage/home/knostroverkhii/=workspace/input'
list_of_lists = []
for filename in os.listdir(input_path):
    if filename.endswith(".cool"):
        arguments_list = [input_path + "/" + filename, output_path + "/d" + filename]
        list_of_lists.append(arguments_list)

for arguments_list in list_of_lists:
    worker(arguments_list)

print(colored("SCV: 'Job finished!'", 'green'))