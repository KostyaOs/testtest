import cooler
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored
import numpy as np
import math
import os


files = os.listdir('input')
frame1 = pd.read_csv('input/' + files[0])
frame2 = pd.read_csv('input/' + files[1])
final = frame1.add(frame2)
final = final.divide(2)
#final.to_csv('output/' + files[0] + '+' + files[1] + '.csv')
final.to_csv('output/final.csv')