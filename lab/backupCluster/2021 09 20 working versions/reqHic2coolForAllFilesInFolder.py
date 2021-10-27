import os
from hic2cool import hic2cool_convert

files = os.listdir('input')

print('check that you have output folder in the same place where script is located')
print('if you do - press "y" to continue')
if input() != 'y':
    print("you typed not 'y' - aborting script")
    exit()

for file in files:
    infile = 'input/' + file
    outfile = 'output/' + file[:file.find('.hic')]
    hic2cool_convert(infile, outfile, 250000)
    print('finished converting', file)
