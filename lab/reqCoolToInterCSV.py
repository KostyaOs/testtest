import cooler
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored
import numpy as np
import math
import os

# read cool file
clr = cooler.Cooler(sys.argv[1])

# check for presence of Y chromosome
chromnames_list = clr.chromnames
if chromnames_list.count('Y') == 0:
    Y_presence = 'n'
else:
    Y_presence = 'y'

# find out how many valid bins in each chromosome
A = clr.matrix(balance=True)[:,:]  # get matrix of balanced values
A[~np.isfinite(A)] = 0  # change non-numbers to be zeros
bins_checklist = np.sum(A, axis=0) != 0  # [ True  True  True ...  True  True False]
binsize = clr.binsize
chromsizes_list = clr.chromsizes  # two column table: first is chromosome name, second is its length is nucleotides
nvalid_list = []  # it will contain amounts of valid pixels for each chromosome
i = 0
j = 0
for chr in chromnames_list:
    chrom_binsize = math.ceil(chromsizes_list[i] / binsize)
    i += 1
    nvalid = bins_checklist[j: j + chrom_binsize].sum()
    j += chrom_binsize
    nvalid_list.append(nvalid)
amount_of_chromosomes = len(nvalid_list)

# create data frame (24*24 or 23*23) where elements are A * B, where A and B are amounts of valid bins for
# chromosomes a and b respectively
valid_bins_matrix = [[0] * amount_of_chromosomes for i in range(amount_of_chromosomes)]  # make zero matrix 24*24 (
# or 23*23)
for i in range(amount_of_chromosomes):
    for j in range(amount_of_chromosomes):
        valid_bins_matrix[i][j] = nvalid_list[i] * nvalid_list[j]  # fill it with amounts of pixels
df_valid_bins_matrix = pd.DataFrame(data=valid_bins_matrix)  # convert it do data frame
if Y_presence != 'y':
    orderCorrection = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 18, 21, 20, 22]
else:
    orderCorrection = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 18, 21, 20, 22, 23]
df_valid_bins_matrix = df_valid_bins_matrix[orderCorrection]
df_valid_bins_matrix = df_valid_bins_matrix.reindex(orderCorrection)

# choose value column to make map from and calculate total amount of contacts (raw or balanced) to use as a norm
value_column = 'balanced'
extra_column = 'count'
mtx = clr.matrix(balance=True)[:]
mtx[~np.isfinite(mtx)] = 0  # change non-numbers to be zeros
norm = mtx.sum()

mtx = clr.matrix(balance=True, as_pixels=True, join=True)[:, :]
mtx[value_column] = mtx[value_column].fillna(value=0)  # change non-numbers to be zeros
mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', extra_column])  # remove these columns
trans_contacts = mtx[mtx['chrom1'] != mtx['chrom2']]  # select trans contacts
sum = trans_contacts.groupby(by=['chrom1', 'chrom2']).sum()  # merge all contacts for a given pair of chromosomes
sum.to_csv(file + '.csv')
sum = pd.read_csv(file + '.csv')

# 2021 06 27 depth normalization
sum[value_column] = sum[value_column] / norm

# names of chromosomes in new_indexes should be the same as in .cool file; otherwise table values get lost
if Y_presence != 'y':
    new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', 'X']
else:
    new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '19', '20', '21', '22', 'X', 'Y']
sum = sum.pivot(index='chrom1', columns='chrom2')

sum.columns = sum.index
sum = sum.where(sum != 0, sum.T)
sum = sum.reindex(index=new_indexes, columns=new_indexes)
sum = pd.DataFrame(sum.values / df_valid_bins_matrix.values, columns=new_indexes, index=new_indexes)

output_path = file[file.find('/'):] + '.csv'
sum.to_csv(output_path)

#fig.figure.savefig(file + '.png')

#os.remove(file + '.csv')
print(colored("SCV: 'Job finished!'", 'green'))
