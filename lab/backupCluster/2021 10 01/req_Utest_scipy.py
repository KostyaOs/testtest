import pandas as pd
from termcolor import colored
import os
from scipy.stats import mannwhitneyu


def mainfunc(normsF, casesF):
    # check for ties
    merge = normsF + casesF
    if len(merge) != len(set(merge)):
        print(colored("there are ties in samples, aborting script", 'red'))
        exit()

    U1, p = mannwhitneyu(normsF, casesF)
    U2 = len(normsF) * len(casesF) - U1

    if p > 0.05:
        hypothesis = 'same'
    else:
        hypothesis = 'different'

    rslt = [min(U1, U2), max(U1, U2), p, hypothesis]
    return rslt


# returns codename of specimen
def key(cool_file):
    return cool_file[:cool_file.find('.cool')]


# returns pathology of specimen
def pathology(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'pathology'].iloc[0]


# returns sex of specimen
def sex(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'sex'].iloc[0]

# returns celltype of specimen
def celltype(codeF):
    return specimenInfo.loc[specimenInfo['code'] == codeF, 'cellType'].iloc[0]


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

groupgender, groupcelltype, grouppathology = input("Specify group by entering gender and cell type. Then enter "
                                                   "pathology. Split with spaces\n").split()
specimenInfo = pd.read_csv('/mnt/storage/home/knostroverkhii/workspace/specimenInfo.csv')  # open specimen info table
inpath = '/mnt/storage/home/knostroverkhii/workspace/input'
outpath = '/mnt/storage/home/knostroverkhii/workspace/output'
filenames = os.listdir(inpath)
filenames.sort()
normspecimens = []
casespecimens = []
for filename in filenames:
    if filename.endswith('.cool'):
        code = key(filename)
        gender = sex(code)
        cellclass = celltype(code)
        if gender == groupgender and cellclass == groupcelltype:
            patho = pathology(code)
            if patho == 'none':
                normspecimens.append(code)
            elif patho == grouppathology:
                casespecimens.append(code)
df_dict = {}
for specimen in normspecimens + casespecimens:
    df = pd.read_csv(inpath + '/' + specimen + ',finalcontacts.csv')  # open specimen info table
    df_dict[specimen] = df

Umin_list = []
Umax_list = []
p_list = []
hypothesis_list = []
for i in df.index:
    norms = []
    cases = []
    for specimen in normspecimens:
        norms.append(df_dict[specimen]['balanced'][i])
    for specimen in casespecimens:
        cases.append(df_dict[specimen]['balanced'][i])
    parameters = mainfunc(norms, cases)
    Umin_list.append(parameters[0])
    Umax_list.append(parameters[1])
    p_list.append(parameters[2])
    hypothesis_list.append(parameters[3])
    print(colored('chromosome pair number ' + str(i + 1) + " has been processed", 'blue'))

# make result.csv
result = df.copy()
result = result.drop(columns = ['balanced'])
addon = pd.DataFrame(list(zip(Umin_list, Umax_list, p_list, hypothesis_list)), columns =['Umin', 'Umax', 'pvalue', 'hypothesis'])
result = result.join(addon)
result.to_csv(outpath + '/U-test scipy for ' + grouppathology + '.csv', index=False, index_label=False)
# check scipy by handmade U test script?

print(colored("script fully finished", 'green'))

