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
    subprocess.run(["cooler", "balance", "--force", cool_file])
    print(colored("file has been processed", 'yellow'))


#show what is in input (files AND directories)
input_path = 'input'
contents = os.listdir(input_path) # returns list
if not len(contents):
    print(colored("Input directory is empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'yellow'))
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
onlyfiles = [input_path + "/" + f for f in listdir(input_path) if isfile(join(input_path, f))]

for file in onlyfiles:
    worker(file)

print(colored("SCV: 'Job finished!'", 'green'))