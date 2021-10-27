import pandas as pd
from termcolor import colored
import os


def mainfunc(normsF, casesF):
    # check for ties
    merge = normsF + casesF
    if len(merge) != len(set(merge)):
        print(colored("there are ties in samples, aborting script", 'red'))
        exit()
    merge.sort()
    affiliation = []
    for element in merge:
        if element in normsF:
            affiliation.append('norms')
        elif element in casesF:
            affiliation.append('cases')
    df = pd.DataFrame(list(zip(merge, affiliation)), columns=['element', 'sample'])
    #print(df)  # for debug
    rnorms = 0
    rcases = 0
    for idx in df.index:
        if df['sample'][idx] == 'norms':
            rnorms += idx + 1
        elif df['sample'][idx] == 'cases':
            rcases += idx + 1

    nnorms = len(norms)
    ncases = len(cases)
    unorms = nnorms * ncases - rnorms + 0.5 * nnorms * (nnorms + 1)
    ucases = nnorms * ncases - rcases + 0.5 * ncases * (ncases + 1)

    u = min(unorms, ucases)
    if u > 0:  # 0 is critical U value when n1, n2 = 5, 3 and p value = 0,05
        hypothesis = 'same'
    else:
        hypothesis = 'different'
   # print(df)  # for debug
  #  print(nnorms)  # for debug
  #  print(ncases)  # for debug
 #   print(rnorms)  # for debug
 #   print(rcases)  # for debug
 #   print(unorms)  # for debug
  #  print(ucases)  # for debug
  #  print(u)  # for debug
  #  print(hypothesis)  # for debug
 #   print(unorms + ucases)  # for debug
 #   print(nnorms * ncases)  # for debug

    rslt = [u, max(unorms, ucases), hypothesis]
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
#groupgender, groupcelltype, grouppathology = 'female', 'chorion', '13+'  # for debug

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
hypothesis_list = []
#j = 1  # for debug
for i in df.index:
 #   if j == 3:  # for debug
   #     exit()  # for debug
    norms = []
    cases = []
    for specimen in normspecimens:
        norms.append(df_dict[specimen]['balanced'][i])
    for specimen in casespecimens:
        cases.append(df_dict[specimen]['balanced'][i])
    parameters = mainfunc(norms, cases)
    Umin_list.append(parameters[0])
    Umax_list.append(parameters[1])
    hypothesis_list.append(parameters[2])
    print(colored('chromosome pair number ' + str(i + 1) + " has been processed", 'blue'))
#    j += 1  # for debug

# make result.csv
result = df.copy()
result = result.drop(columns=['balanced'])
addon = pd.DataFrame(list(zip(Umin_list, Umax_list, hypothesis_list)), columns=['Umin', 'Umax', 'hypothesis'])
result = result.join(addon)
result.to_csv(outpath + '/U-test handmade for ' + grouppathology + '.csv', index=False, index_label=False)
# check scipy by handmade U test script?

print(colored("script fully finished", 'green'))
