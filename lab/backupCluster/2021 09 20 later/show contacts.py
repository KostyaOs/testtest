import cooler
import sys
import pandas as pd
from termcolor import colored

# get input
# print(colored('type input path, output path (without extensions), chromosome, numerator, denominator', 'yellow'))
# input_list = list(map(str, input().split()))
input_path = sys.argv[1]
input_chr = sys.argv[2]

# get source data for new cool file
clr = cooler.Cooler(input_path)  # read cool file

dfb = clr.bins()[:]  # extract bins data
select_bins = dfb[dfb['chrom'] == 'chr' + input_chr]  # select specified chromosome bins
ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins
print(colored("SCV: 'below is bin table '", 'yellow'))
print(dfb)

dfp = clr.matrix()[:]  # extract pixels data
print(colored("SCV: 'below is all selection'",'yellow'))
print(dfp)

print(colored("SCV: 'below are ids of first and last bins in chosen chromosome'",'yellow'))
print(ids[0], ids[-1])

print(colored("SCV: 'below is bin1_id selection'",'yellow'))
selection = dfp[dfp['bin1_id'].isin(ids)]
print(selection)

print(colored("SCV: 'below is bin2_id selection'",'yellow'))
selection = dfp[dfp['bin2_id'].isin(ids)]
print(selection)

print(colored("SCV: 'Job finished!'", 'green'))