import cooler
import pandas as pd
from termcolor import colored
import os
import shutil


def key(fileF):  # returns code of specimen
    return fileF[:fileF.find('.cool')]


def sex(codeF):  # returns sex of specimen
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'sex'].iloc[0]


def mainfunc(sourceF, destinationF):  # makes new file with no chromosome Y
    clr = cooler.Cooler(sourceF)

    dfb = clr.bins()[:]  # extract bins data
    select_bins = dfb[dfb['chrom'] == 'Y']  # select specified chromosome bins
    ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins
    dfb = dfb.drop(ids)  # delete rows with Y chromosome

    dfp = clr.pixels()[:]  # extract pixels data
    dfp = dfp.drop(dfp.loc[dfp['bin1_id'].isin(ids)].index)  # delete portion of rows with Y chromosome
    dfp = dfp.drop(dfp.loc[dfp['bin2_id'].isin(ids)].index)  # delete the rest of rows with Y chromosome

    cooler.create_cooler(cool_uri=destinationF, bins=dfb, pixels=dfp)  # make new cool file


# check that output folder is empty
output_path = '/mnt/storage/home/knostroverkhii/workspace/output'
contents = os.listdir(output_path)  # returns list
if len(contents):
    contents.sort()
    print(colored("Output directory is not empty, below are it's contents:", 'blue'))
    for file in contents:
        print(file)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()

# show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
contents = os.listdir(input_path)  # returns list
if not len(contents):
    print(colored("Input directory is empty. Fill it if you wish to continue. Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()
else:
    contents.sort()
    print(colored("Below are contents of input folder:", 'blue'))
    for file in contents:
        print(file)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()

specimenInfo = pd.read_csv('specimenInfo.csv')  # load specimen info table
files = os.listdir(input_path)  # make list of files in input folder
for file in files:
    if file.endswith(".cool"):  # if file is '.cool' file
        code = key(file)  # code of specimen
        source = input_path + "/" + file  # path to input file
        destination = output_path + "/" + file  # path to output file
        if sex(code) == 'female':  # if specimen is female
            mainfunc(source, destination)  # send file to have Y chromosome deleted
        else:
            shutil.move(source, destination)  # just move file to output folder, without changing it anyhow
        print(colored("file has been processed", 'blue'))
