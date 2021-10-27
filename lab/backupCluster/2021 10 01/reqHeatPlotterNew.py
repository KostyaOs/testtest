import cooler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored
import re
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def cut_extension(path_func):
    return path_func[:path_func.find('.')]


def mainfunc(inpathF, filenameF, outpathF):
    mtx = pd.read_csv(inpathF + '/' + filenameF, dtype={'chrom1': str, 'chrom2': str})
    chroms = mtx['chrom1'].unique().tolist()
    chroms += mtx['chrom2'].unique().tolist()
    chroms = list(set(chroms))
    chroms.sort(key=natural_keys)
    print(chroms)

    # make zero filled frame nchr * nchr where indexes and columns are names of chr
    mtx2 = pd.DataFrame(0.0, index=chroms, columns=chroms)
    # exit()
    print(mtx2)

    for i in mtx.index:
        contacts = mtx['balanced'][i]
        # if pd.notna(contacts):
        chrom1 = mtx['chrom1'][i]
        chrom2 = mtx['chrom2'][i]
        # mtx2.iloc[chrom1, mtx2.columns.get_loc(chrom2)] = contacts
        # mtx2.at[chrom1, chrom2] = contacts
        mtx2[chrom1][chrom2] += contacts
        mtx2[chrom2][chrom1] += contacts
        # print(contacts, type(chrom1), type(chrom2))
        # print(mtx2)
        # print(type(chroms[3]))
        # print(mtx2[chrom2][chrom1])
        # print(type(contacts))
        # exit()
    print(mtx2)
    plt.clf()
    plt.cla()
    print(mtx2)
    fig = sns.heatmap(data=mtx2, cmap='Reds')
    #    fig = sns.heatmap(data=sum, vmin=input_vmin, vmax=input_vmax, cmap='Reds')

    output_path = outpathF + '/' + cut_extension(filenameF) + '_plot.png'
    fig.figure.savefig(output_path)


inpath = '/mnt/storage/home/knostroverkhii/workspace/input'
outpath = '/mnt/storage/home/knostroverkhii/workspace/output'
filenames = os.listdir(inpath)
filenames.sort()
for filename in filenames:
    if filename.endswith('.csv'):
        mainfunc(inpath, filename, outpath)
        print(colored("frame is constructed", 'blue'))
print(colored("script finished", 'green'))
