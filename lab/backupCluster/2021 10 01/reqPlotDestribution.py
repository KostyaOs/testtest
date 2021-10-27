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

cools = os.listdir('/mnt/storage/home/knostroverkhii/workspace/input')
if not os.path.exists('/mnt/storage/home/knostroverkhii/workspace/output/notdifferences'):
    os.mkdir('/mnt/storage/home/knostroverkhii/workspace/output/notdifferences')

for cool in cools:
    command = 'echo "source /mnt/storage/home/knostroverkhii/anaconda3/envs/fromAlina/bin/activate; python workspace/reqPlotDestribution2.py ' + cool + '" | qsub -l select=1:ncpus=1:mem=6gb,walltime=0:20:0'
    os.system(command)

