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


specimenInfo = pd.read_csv('specimenInfo.csv')

sex = []
for idx in specimenInfo.index:
    if specimenInfo['sexChromosomes'][idx].count('y') > 0:
        sex.append('male')
    else:
        sex.append('female')

specimenInfo['sex'] = sex

specimenInfo.to_csv('specimenInfoNew.csv')