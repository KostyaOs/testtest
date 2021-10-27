import cooler
import sys
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join


def worker(input_list):
    in_path = input_list[0]
    out_path = input_list[1]
    multiplier = 40  # how much should binsize increase

    nnz = cooler.Cooler(in_path).info["nnz"]  # get total amount of pixels
    cooler.coarsen_cooler(in_path, out_path, multiplier, nnz)  # make new cool file

    print(colored("file has been processed", 'blue'))


#check that output folder is empty
output_path = '/mnt/storage/home/knostroverkhii/=workspace/output'
contents = os.listdir(output_path) # returns list
if len(contents):
    print(colored("Directory is not empty, below are it's contents:", 'blue'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()

#show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/=workspace/input'
contents = os.listdir(input_path) # returns list
if not len(contents):
    print(colored("Output directory empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'blue'))
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
        arguments_list = [input_path + "/" + filename, output_path + "/" + filename]
        list_of_lists.append(arguments_list)

for arguments_list in list_of_lists:
    worker(arguments_list)

print(colored("SCV: 'Job finished!'", 'green'))