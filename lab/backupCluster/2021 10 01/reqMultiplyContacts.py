import cooler
import pandas as pd
from termcolor import colored
import os
import shutil


# below is explanation on basic idea for functions that multiply contacts
# we will make new cool file, for that cooler needs bins data and pixels data
# so we extract those from initial cool file, then make changes in them (well, honestly we only change pixels data)
# we get indexes of bins for chromosome that we want to multiply
# then we use these indexes to select pixels with that chromosome
# then we multiply selected pixels
# finally we send bins data and edited pixels data to be used to make a new file
# for fractional multipliers for pixels with lowest sums (= 1 (2)) we skip some pixels or do other subtle change
# because trans pixels mainly have sum of 1, at least in our combination of  sequencing depth and resolution


#   function that makes actually applies multiplies, but only for aneuploids
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
                # change every third 1 to 0
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
                # change every second 1 to 0
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

    cooler.create_cooler(cool_uri=outpath, bins=dfb, pixels=dfp)  # make new cool file


#   function that makes actually applies multiplies, but only for polyploids
def workerPoly(inpath, outpath, dictionarY):
    # open cool file
    clr = cooler.Cooler(inpath)
    dfb = clr.bins()[:]  # extract bins data
    dfp = clr.pixels()[:]  # extract pixels data
    print(dfb)

    # deal with gonosomes
    for keY in dictionarY.keys():
        print(keY)
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
                # change every third 1 to 0
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
                # change every second 1 to 0
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
    for chromosome in range(1, 23):  # range(1, 23) is [1, ... , 22]
        select_bins = dfb[dfb['chrom'] == str(chromosome)]  # select specified chromosome bins
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
        dfp.loc[indexes, 'count'] *= 2 / 3
        print('processed chromosome ' + str(chromosome))

    # make new cool file
    cooler.create_cooler(cool_uri=outpath, bins=dfb, pixels=dfp)


# returns codename of specimen
def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


# returns pathology of specimen
def pathology(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'pathology'].iloc[0]


# returns sex of specimen
def sex(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'sex'].iloc[0]


# returns set of gonosomes of specimen
def sexChromosomes(code):
    return specimenInfo.loc[specimenInfo['code'] == code, 'sexChromosomes'].iloc[0]


# function that is used to determine what multiplier to apply for aneuploid chromosome
def aneuCounter(aneu, listF):
    result = ''
    if aneu[0] == '+' or aneu[0] == '-':
        for i in range(len(aneu)):
            if aneu[i] == '+' or aneu[i] == '-':
                result += aneu[i]
            else:
                if len(aneu[i:]) > 0:
                    aneuCounter(aneu[i:], listF)
                break
        listF.append(result)
    if aneu[0] != '+' and aneu[0] != '-':
        for i in range(len(aneu)):
            if aneu[i] != '+' and aneu[i] != '-':
                result += aneu[i]
            else:
                if len(aneu[i:]) > 0:
                    aneuCounter(aneu[i:], listF)
                break
        listF.append(result)


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
    print(colored("Input directory is empty. Fill it if you wish to continue. Continue (Enter) or exit (Ctrl + C)?",
                  'blue'))
    input()
else:
    contents.sort()
    print(colored("Below are contents of input folder:", 'blue'))
    for file in contents:
        print(file)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()

specimenInfo = pd.read_csv('specimenInfo.csv')  # open specimen info table
files = os.listdir(input_path)
files.sort()
for file in files:
    if file.endswith(".cool"):  # if file is '.cool' file
        specimen = key(file)    # code of specimen
        patho = pathology(specimen)     # pathology of specimen
        if patho == 'none':     # if specimen is a norm
            shutil.move(input_path + "/" + file, output_path + "/" + file)  # just move file to output folder, without changing it anyhow
        else:
            # make dictionary {chr: multiplier}
            dictionary = {}

            # decide on gonosomes
            if sex(specimen) == 'male':
                set = sexChromosomes(specimen)
                x = set.count('x')  # amount of X chromosomes of the specimen
                y = set.count('y')  # amount of Y chromosomes of the specimen
                if x > 1:
                    dictionary['X'] = 1 / x  # remember to multiply it by 1 / x
                if y != 1:  # if it's a male than there's definitely at least 1 y chromosome
                    dictionary['Y'] = 1 / y  # remember to multiply it by 1 / y
            else:
                set = sexChromosomes(specimen)
                x = set.count('x')  # amount of X chromosomes of the specimen
                if x != 0 and x != 2:
                    dictionary['X'] = 2 / x  # remember to multiply it by 2 / x
            # decide on autosomes
            if patho == 'polyploidy':
                # send file to be processed
                workerPoly(input_path + '/' + file, output_path + '/' + file, dictionary)
            else:
                # get list of aneuploidies [chromosome1, sign1, ... , chromosomeN, signN]
                chromnsign = []
                aneuCounter(patho, chromnsign)     # fill the list
                chromnsign = chromnsign[::-1]

                # remove gonosomes, X comes before Y, so no need to write Y
                if chromnsign.count('x') > 0:
                    i = 0
                    while chromnsign[i] != 'x':
                        i += 1
                    chromnsign = chromnsign[:i]

                # fill dictionary with pairs (chromosome, multiplier)
                i = 0   # counter for chromosome name
                j = 1   # counter for aneuploidy sign (+ / -)
                while j + 1 <= len(chromnsign):
                    if chromnsign[j] == '-':   # if it is monosomy (previously it was 'if listing[j][0] == '-' and len(listing[j]) == 1:')
                        multiplier = 2
                    if chromnsign[j][0] == '+':    # if it is tri(tetra, ...)somy
                        multiplier = 2 / (2 + len(chromnsign[j]))  # len(listing[j]) is how many extra copies of chromosome there are
                    else:
                        print(colored('Encountered unexpected aneuploidy for specimen ' + specimen + ". Here it's chromnsign list " + str(chromnsign), 'red'))
                        exit()
                    dictionary[chromnsign[i]] = multiplier  # remember to multiply chromosome by newly calculated multiplier
                    i += 2  # previously it was '+= 1' but that should be wrong
                    j += 2  # previously it was '+= 1' but that should be wrong
                workerAneu(input_path + '/' + file, output_path + '/' + file, dictionary)   # send file to be processed
        print(colored("file has been processed", 'blue'))
