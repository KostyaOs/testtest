import os

files = os.listdir('input')

specimens = []
total = []
for file in files:
    specimen = file[:file.find('.txt')]
    specimens.append(specimen)
    with open('input/' + file, 'rt') as f:
        lines = f.readlines()
        total.append(lines[0])

with open('output/ExtraTotal.csv', 'wt') as data_file:
    data_file.write('specimen;')
    for specimen in specimens:
        data_file.write(f'{specimen};')
    data_file.write('\n')
    data_file.write('total;')
    for value in total:
        data_file.write(f'{value};')

