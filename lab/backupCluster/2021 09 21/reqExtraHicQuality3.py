import os

files = os.listdir('input')
files.sort()

choice = 0

# dictionary that holds lists each of which will be a line in final .csv
dictionary = {}
file = files[0]
dictionary['specimens'] = []
with open('input/' + file, 'rt') as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        dictionary[i] = []
        i += 1

for file in files:
    specimen = file[:file.find('.txt')]
    dictionary['specimens'].append(specimen)
    with open('input/' + file, 'rt') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            if line.endswith('\n'):
                dictionary[i].append(line.rstrip('\n'))
            else:
                dictionary[i].append(line)
            i += 1

with open('output/ExtraHicQuality.csv', 'wt') as data_file:
    for key in dictionary.keys():
        data_file.write(f'{key};')
        for value in dictionary[key]:
            data_file.write(f'{value};')
        data_file.write('\n')


if choice == 'DE, total,DEfrac, cis, trans':
    specimens = []
    DE = []
    total = []
    DEfrac = []
    cis = []
    trans = []
    for file in files:
        specimen = file[:file.find('.txt')]
        specimens.append(specimen)
        with open('input/' + file, 'rt') as f:
            lines = f.readlines()
            DE.append(lines[0].rstrip('\n'))
            total.append(lines[1].rstrip('\n'))
            DEfrac.append(lines[2].rstrip('\n'))
            cis.append(lines[3].rstrip('\n'))
            trans.append(lines[4])

    with open('output/Extra.csv', 'wt') as data_file:
        data_file.write(';')
        for specimen in specimens:
            data_file.write(f'{specimen};')
        data_file.write('\n')
        data_file.write('DE_pairs;')
        for value in DE:
            data_file.write(f'{value};')
        data_file.write('\n')
        data_file.write('total;')
        for value in total:
            data_file.write(f'{value};')
        data_file.write('\n')
        data_file.write('DE_fraction;')
        for value in DEfrac:
            data_file.write(f'{value};')
        data_file.write('\n')
        data_file.write('Cis_Hi-C_pairs;')
        for value in cis:
            data_file.write(f'{value};')
        data_file.write('\n')
        data_file.write('Trans_Hi-C_pairs;')
        for value in trans:
            data_file.write(f'{value};')
        data_file.write('\n')