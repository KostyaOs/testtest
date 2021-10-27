import cooler
import sys
import pandas as pd
from termcolor import colored
import os
from os import listdir
from os.path import isfile, join
import shutil


def workerAneu(inpath, outpath, dictionarY):
    # open cool file
    clr = cooler.Cooler(inpath)
    dfb = clr.bins()[:]  # extract bins data
    dfp = clr.pixels()[:]  # extract pixels data

    # multiply contacts
    for keY in dictionarY.keys():
        select_bins = dfb[dfb['chrom'] == keY]  # select specified chromosome bins
        ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

        multiplieR = dictionarY[keY]
        if multiplieR < 1:
            if multiplieR == 2 / 3:
                select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] > 2]
                select_pixels_ones = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 1]
                select_pixels_twos = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 2]
                indexes = select_pixels.index.tolist()
                indexes_ones = select_pixels_ones.index.tolist()
                indexes_twos = select_pixels_twos.index.tolist()

                select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] > 2]
                select_pixels_ones = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 1]
                select_pixels_twos = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 2]
                indexes = indexes + select_pixels.index.tolist()
                indexes_ones = indexes_ones + select_pixels_ones.index.tolist()
                indexes_twos = indexes_twos + select_pixels_twos.index.tolist()

                indexes_ones = list(dict.fromkeys(indexes_ones))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_ones)
                if NexceptionalIndexes > 0:
                    indexes_ones2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 3 == 0:
                            indexes_ones2.append(indexes_ones[t])
                        t += 1
                        if position % 1000 == 0:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_ones2, 'count'] *= 0

                # turn every 2,2,2 (6) into 2,1,1 (4)
                indexes_twos = list(dict.fromkeys(indexes_twos))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_twos)
                if NexceptionalIndexes > 0:
                    indexes_twos2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 2 == 0 or position % 3 == 0:
                            indexes_twos2.append(indexes_twos[t])
                        t += 1
                        if position % 1000 == 0:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_twos2, 'count'] *= 0.5

                indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
                dfp.loc[indexes, 'count'] *= multiplieR

            elif multiplieR == 1 / 2:
                select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] > 1]
                select_pixels_ones = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 1]

                indexes = select_pixels.index.tolist()
                indexes_ones = select_pixels_ones.index.tolist()

                select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] > 1]
                select_pixels_ones = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 1]
                indexes = indexes + select_pixels.index.tolist()
                indexes_ones = indexes_ones + select_pixels_ones.index.tolist()

                indexes_ones = list(dict.fromkeys(indexes_ones))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_ones)
                if NexceptionalIndexes > 0:
                    indexes_ones2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 2 == 0:
                            indexes_ones2.append(indexes_ones[t])
                        t += 1
                        if position % 1000 == 0:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_ones, 'count'] *= 0
                indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
                dfp.loc[indexes_ones2, 'count'] *= multiplieR

            else:
                print('I did not see that multiplier coming: ' + multiplieR + '. Aborting program now')
                exit()

        else:
            select_pixels = dfp[dfp['bin1_id'].isin(ids)]
            indexes = select_pixels.index.tolist()
            select_pixels = dfp[dfp['bin2_id'].isin(ids)]
            indexes = indexes + select_pixels.index.tolist()
            indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
            dfp.loc[indexes, 'count'] *= multiplieR
        print('processed chromosome ' + keY)

    cooler.create_cooler(cool_uri=outpath, bins=dfb, pixels=dfp)  # make new cool file
    print(colored("file has been processed", 'blue'))


def workerPoly(inpath, outpath, dictionarY):
    # open cool file
    clr = cooler.Cooler(inpath)
    dfb = clr.bins()[:]  # extract bins data
    dfp = clr.pixels()[:]  # extract pixels data

    # deal with gonosomes
    for keY in dictionarY.keys():
        select_bins = dfb[dfb['chrom'] == keY]  # select specified chromosome bins
        ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

        multiplieR = dictionarY[keY]
        if multiplieR < 1:
            if multiplieR == 2 / 3:
                select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] > 2]
                select_pixels_ones = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 1]
                select_pixels_twos = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 2]
                indexes = select_pixels.index.tolist()
                indexes_ones = select_pixels_ones.index.tolist()
                indexes_twos = select_pixels_twos.index.tolist()

                select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] > 2]
                select_pixels_ones = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 1]
                select_pixels_twos = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 2]
                indexes = indexes + select_pixels.index.tolist()
                indexes_ones = indexes_ones + select_pixels_ones.index.tolist()
                indexes_twos = indexes_twos + select_pixels_twos.index.tolist()

                indexes_ones = list(dict.fromkeys(indexes_ones))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_ones)
                if NexceptionalIndexes > 0:
                    indexes_ones2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 3 == 0:
                            indexes_ones2.append(indexes_ones[t])
                        t += 1
                        if position % 10000000:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_ones2, 'count'] *= 0

                # turn every 2,2,2 (6) into 2,1,1 (4)
                indexes_twos = list(dict.fromkeys(indexes_twos))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_twos)
                if NexceptionalIndexes > 0:
                    indexes_twos2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 2 == 0 or position % 3 == 0:
                            indexes_twos2.append(indexes_twos[t])
                        t += 1
                        if position % 1000 == 0:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_twos2, 'count'] *= 0.5

                indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
                dfp.loc[indexes, 'count'] *= multiplieR

            elif multiplieR == 1 / 2:
                select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] > 1]
                select_pixels_ones = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 1]

                indexes = select_pixels.index.tolist()
                indexes_ones = select_pixels_ones.index.tolist()

                select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] > 1]
                select_pixels_ones = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 1]
                indexes = indexes + select_pixels.index.tolist()
                indexes_ones = indexes_ones + select_pixels_ones.index.tolist()

                indexes_ones = list(dict.fromkeys(indexes_ones))  # remove duplicates from indexes list
                NexceptionalIndexes = len(indexes_ones)
                if NexceptionalIndexes > 0:
                    indexes_ones2 = []
                    t = 0
                    while t != NexceptionalIndexes:
                        position = t + 1
                        if position % 2 == 0:
                            indexes_ones2.append(indexes_ones[t])
                        t += 1
                        if position % 1000 == 0:
                            print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
                    dfp.loc[indexes_ones2, 'count'] *= 0
                indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
                dfp.loc[indexes, 'count'] *= multiplieR

            else:
                print('I did not see that multiplier coming: ' + multiplieR + '. Aborting program now')
                exit()

        else:
            select_pixels = dfp[dfp['bin1_id'].isin(ids)]
            indexes = select_pixels.index.tolist()
            select_pixels = dfp[dfp['bin2_id'].isin(ids)]
            indexes = indexes + select_pixels.index.tolist()
            indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
            dfp.loc[indexes, 'count'] *= multiplieR
        print('processed chromosome ' + keY)

    # deal with autosomes
    for i in range(1, 23):
        select_bins = dfb[dfb['chrom'] == str(i)]  # select specified chromosome bins
        ids = select_bins.index.tolist()  # make list with ids of specified chromosome bins

        select_pixels = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] > 2]
        select_pixels_ones = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 1]
        select_pixels_twos = dfp[dfp['bin1_id'].isin(ids)][dfp['count'] == 2]
        indexes = select_pixels.index.tolist()
        indexes_ones = select_pixels_ones.index.tolist()
        indexes_twos = select_pixels_twos.index.tolist()

        select_pixels = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] > 2]
        select_pixels_ones = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 1]
        select_pixels_twos = dfp[dfp['bin2_id'].isin(ids)][dfp['count'] == 2]
        indexes = indexes + select_pixels.index.tolist()
        indexes_ones = indexes_ones + select_pixels_ones.index.tolist()
        indexes_twos = indexes_twos + select_pixels_twos.index.tolist()

        indexes_ones = list(dict.fromkeys(indexes_ones))  # remove duplicates from indexes list
        NexceptionalIndexes = len(indexes_ones)
        if NexceptionalIndexes > 0:
            indexes_ones2 = []
            t = 0
            while t != NexceptionalIndexes:
                position = t + 1
                if position % 3 == 0:
                    indexes_ones2.append(indexes_ones[t])
                t += 1
                if position % 1000 == 0:
                    print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
            dfp.loc[indexes_ones, 'count'] *= 0

        # turn every 2,2,2 (6) into 2,1,1 (4)
        indexes_twos = list(dict.fromkeys(indexes_twos))  # remove duplicates from indexes list
        NexceptionalIndexes = len(indexes_twos)
        if NexceptionalIndexes > 0:
            indexes_twos2 = []
            t = 0
            while t != NexceptionalIndexes:
                position = t + 1
                if position % 2 == 0 or position % 3 == 0:
                    indexes_twos2.append(indexes_twos[t])
                t += 1
                if position % 1000 == 0:
                    print('processed ' + str(position) + ' bin pairs out of ' + str(NexceptionalIndexes))
            dfp.loc[indexes_twos2, 'count'] *= 0.5

        indexes = list(dict.fromkeys(indexes))  # remove duplicates from indexes list
        dfp.loc[indexes, 'count'] *= 2 / 3
        print('processed chromosome ' + str(i))

    # make new cool file
    cooler.create_cooler(cool_uri=outpath, bins=dfb, pixels=dfp)
    print(colored("file has been processed", 'blue'))


def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


def pathology(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'pathology'].iloc[0]


def sex(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0]


def sexChromosomes(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'sexChromosomes'].iloc[0]


def aneuCounter(aneu, listingg):
    result = ''
    if aneu[0] == '+' or aneu[0] == '-':
        for i in range(len(aneu)):
            if aneu[i] == '+' or aneu[i] == '-':
                result += aneu[i]
            else:
                if len(aneu[i:]) > 0:
                    aneuCounter(aneu[i:], listingg)
                break
        listingg.append(result)
    if aneu[0] != '+' and aneu[0] != '-':
        for i in range(len(aneu)):
            if aneu[i] != '+' and aneu[i] != '-':
                result += aneu[i]
            else:
                if len(aneu[i:]) > 0:
                    aneuCounter(aneu[i:], listingg)
                break
        listingg.append(result)


# check that output folder is empty
output_path = '/mnt/storage/home/knostroverkhii/workspace/output'
contents = os.listdir(output_path)  # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'yellow'))
    contents.sort()
    for file in contents:
        print(file)
    print(colored("Continue or exit (Ctrl + C)?", 'yellow'))
    input()

# show what is in input (files AND directories)
input_path = '/mnt/storage/home/knostroverkhii/workspace/input'
contents = os.listdir(input_path)  # returns list
if not len(contents):
    print(
        colored("Input directory empty. Press 'y' once you fill it. Press (Ctrl + C) to terminate program.", 'yellow'))
    input()
else:
    print(colored("Below are contents of input folder:", 'yellow'))
    contents.sort()
    for file in contents:
        print(file)
    print(colored("Continue or exit (Ctrl + C)?", 'yellow'))
    input()

specimenInfo = pd.read_csv('specimenInfo.csv')  # open specimen info table
files = os.listdir(input_path)
files.sort()
for file in files:
    if file.endswith(".cool"):
        specimen = key(file)
        patho = pathology(specimen)

        print(specimen)
        print(patho)
        print(sex(specimen))
        print(sexChromosomes(specimen))

        if patho == 'none':
            shutil.move(input_path + "/" + file, output_path + "/" + file)
        else:
            # make dictionary {chr: multiplier}
            dictionary = {}

            # decide on gonosomes
            if sex(specimen) == 'male':
                set = sexChromosomes(specimen)
                x = set.count('x')
                y = set.count('y')

                print(set)
                print(x)
                print(y)
                if x > 1:
                    dictionary['Х'] = 1 / x  # remember to multiply it by 1 / x
                if y != 1:  # if it's a male than there's definitely at least 1 y chromosome
                    dictionary['Y'] = 1 / y  # remember to multiply it by 1 / y
            else:
                set = sexChromosomes(specimen)
                x = set.count('x')
                if x != 0 and x != 2:
                    dictionary['X'] = 2 / x
            # decide on autosomes
            if patho == 'polyploidy':
                # send file to be processed
                workerPoly(input_path + '/' + file, output_path + '/' + file, dictionary)
            else:
                listing = []
                aneuCounter(patho, listing)
                print(listing)
                listing = listing[::-1]
                print(listing)

                # remove gonosomes, X comes before Y, so no need to write Y
                if listing.count('x') > 0:
                    i = 0
                    while listing[i] != 'x':
                        i += 1
                    listing = listing[:i]
                print(listing)

                # fill dictionary with pairs (chromosome, multiplier)
                i = 0
                j = 1
                while j + 1 <= len(listing):
                    if listing[j][0] == '-' and len(listing[j]) == 1:
                        multiplier = 2
                    if listing[j][0] == '+':
                        multiplier = 2 / (2 + len(listing[j]))
                    else:
                        print(colored('encountered unexpected aneuploidy for specimen ' + specimen, 'green'))
                    dictionary[listing[i]] = multiplier
                    i += 1
                    j += 1
                workerAneu(input_path + '/' + file, output_path + '/' + file, dictionary)
            print(dictionary)
            print()

print(colored("SCV: 'Job finished!'", 'green'))
