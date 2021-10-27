import cooler
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored
import numpy as np
import math
import os

file = '3475-G.cool'
sum = pd.read_csv(file + 'new2.csv')
sum = sum[sum['balanced'].notna()]

# names of chromosomes in new_indexes should be the same as in .cool file; otherwise table values get lost
chromnames_list = cooler.Cooler(file).chromnames
if chromnames_list.count('Y') == 0:
    new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', 'X']
else:
    new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', 'X', 'Y']
sum = sum.pivot(index='chrom1', columns='chrom2')

sum.columns = sum.index
sum = sum.where(sum != 0, sum.T)
sum = sum.reindex(index=new_indexes, columns=new_indexes)
sum = pd.DataFrame(sum.values, columns=new_indexes, index=new_indexes)
sum.to_csv(file + 'new3.csv')
plt.cla()
#if automatic_scaling != 'y':
    #fig = sns.heatmap(data=sum, vmin=input_vmin, vmax=input_vmax, cmap='Reds')
#else:
 #   fig = sns.heatmap(data=sum, cmap='Reds')
fig = sns.heatmap(data=sum, cmap='Reds')
output_path = file[:file.find('.cool')] + 'ТУЦ!.png'
fig.figure.savefig(output_path)

#os.remove(file + '.csv')
print(colored("SCV: 'Job finished!'", 'green'))
