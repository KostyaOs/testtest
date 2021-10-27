import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import subprocess


def worker(cool_file):
    command = 'cooler balance --force ' + cool_file
    os.system(command)
    print(colored("file has been processed", 'yellow'))


# show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
contents = os.listdir(input_path)  # returns list
if not len(contents):
    print(
        colored("Input directory empty. Press 'y' once you fill it. Press (Ctrl + C) to terminate program.", 'yellow'))
    input()
else:
    print(colored("Below are contents of input folder:", 'yellow'))
    contents.sort()
    for file in contents:
        print(file)
    print(colored("Continue or exit (Ctrl + C)?", 'yellow'))
    input()

# make list of arguments
onlyfiles = [input_path + "/" + f for f in listdir(input_path) if isfile(join(input_path, f))]

# call worker function for every cool file
files = os.listdir(input_path)
files.sort()
for file in files:
    if file.endswith(".cool"):
        worker(input_path + '/' + file)

print(colored("SCV: 'Job finished!'", 'green'))