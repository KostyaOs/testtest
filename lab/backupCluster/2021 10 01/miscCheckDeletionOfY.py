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

input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
files = os.listdir(input_path)  # make list of files in input folder
for file in files:
    if file.endswith(".cool"):  # if file is '.cool' file
        source = input_path + "/" + file    # path to input file
        clr = cooler.Cooler(source)
        print(file)
        print(clr.bins()[:])

