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

sets = pd.read_csv('transcisbox.csv')
chorion = sets['chorion'].tolist()
fibroblast = sets[sets['fibroblast'].notna()]
fibroblast = fibroblast['fibroblast'].tolist()


data = [chorion, fibroblast]
#fig7, ax7 = plt.subplots()
#ax7.set_title('Multiple Samples with Different sizes')
#ax7.boxplot(data)

fig = plt.figure(figsize=(10, 7))

# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])

# Creating plot
#ax.boxplot(data)

fig, ax = plt.subplots()
ax.set_title('Multiple Samples with Different sizes')
ax.boxplot(data)
#ax.boxplot(data, showfliers=False)


# save plot
plt.savefig('plot.png')


