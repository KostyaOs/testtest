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
df1 = pd.read_csv('input/' + files[0])
df2 = pd.read_csv('input/' + files[1])
print(colored('initial form', 'yellow'))
print(df1)
print(df2)

for col in df1.columns:
    print(col)

df1 = df1.drop(columns=['Unnamed: 0'])
df2 = df2.drop(columns=['Unnamed: 0'])
print(colored('initial form', 'yellow'))
print(df1)
print(df2)

df1 = df1.fiilna(0)
df2 = df2.fiilna(0)
print(colored('new-new form', 'yellow'))
print(df1)
print(df2)

#df_final = df1.add(df1)
#print(final)
#final = final.div(2)
#final.to_csv('output/' + files[0] + '+' + files[1] + '.csv')
#final.to_csv('output/final.csv')