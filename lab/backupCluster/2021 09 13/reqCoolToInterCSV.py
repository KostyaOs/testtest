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

def worker(cool_file):
    # read cool file
    clr = cooler.Cooler(cool_file)

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
    sum.to_csv(cool_file + '.csv')
    sum = pd.read_csv(cool_file + '.csv')

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
    plt.cla()
    print(sum)
    output_path = 'output/' + cool_file[cool_file.find('/'):] + '.csv'
    #sum.to_csv(output_path)
    sum = sum.fillna(0)
    print(sum)

    #fig.figure.savefig(file + '.png')

    #os.remove(file + '.csv')
    print(colored("file has been processed", 'yellow'))

#check that output folder is empty
output_path = 'output'
contents = os.listdir(output_path) # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'yellow'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'yellow'))
    choice = input()
    if choice != 'y':
        exit()

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

print(colored("Job finished!", 'green'))