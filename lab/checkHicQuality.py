import re
import os

externalDictionary = {
    'Unique Reads': {},
    'Inter-chromosomal': {},
    'Intra-chromosomal': {},
    'Chimeric Ambiguous': {},
    'Chimeric Paired': {},
    'Alignable (Normal+Chimeric Paired)': {},
    'PCR Duplicates': {},
    'Intra-fragment Reads': {},
    'Hi-C Contacts': {},
    'Short Range (<20Kb)': {},
    'Long Range (>20Kb)': {},
    'Ligation Motif Present': {},
}

specimens = os.listdir('data')
files = []
for specimen in specimens:
    files.append('data/' + specimen + '/aligned/inter_30.txt')

parametersAll = [
    'Unique Reads',
    'Inter-chromosomal',
    'Intra-chromosomal',
    'Chimeric Ambiguous',
    'Chimeric Paired',
]
parametersPercentWhenSingle = [
    'Alignable (Normal+Chimeric Paired)',
    'PCR Duplicates',
]
parametersPercentFromPair = [
    'Intra-fragment Reads',
    'Hi-C Contacts',
    'Short Range (<20Kb)',
    'Long Range (>20Kb)',
    'Ligation Motif Present'
]

all = '\s*(.*):\s*(.*)'
percentWhenSingle = '\s*(.*):.*\((\d*(.\d*)?)'
percentFromPair = '\s*(.*):.*\/\s*(\d*(\.\d*)?)%'

for file in files:
    with open(file, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    specimen = re.search(all, lines[0]).group(2)
    for parameter in parametersAll:
        for line in lines:
            if re.search(all, line).group(1) == parameter:
                externalDictionary[parameter][specimen] = re.search(all, line).group(2)
    for parameter in parametersPercentWhenSingle:
        for line in lines[7: 10]:
            if re.search(percentWhenSingle, line).group(1) == parameter:
                externalDictionary[parameter][specimen] = re.search(percentWhenSingle, line).group(2)
    for parameter in parametersPercentFromPair:
        for line in lines:
            if line.count('/') > 0:
                if re.search(percentFromPair, line).group(1) == parameter:
                    externalDictionary[parameter][specimen] = re.search(percentFromPair, line).group(2)
        ligationValue = re.search(percentFromPair, lines[15]).group(2)
        externalDictionary['Ligation Motif Present'][specimen] = ligationValue

with open('data.csv', 'wt') as data_file:
    data_file.write(';')
    for specimen in specimens:
        data_file.write(f'{specimen};')
    data_file.write('\n')
    for parameter in externalDictionary:
        data_file.write(f'{parameter};')
        for specimen in externalDictionary[parameter]:
            data_file.write(f'{externalDictionary[parameter][specimen]};')
        data_file.write('\n')

# after finish change ',' to '.', then ';' to ','
