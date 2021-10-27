import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

#check that output folder is empty
output_path = 'output'
contents = os.listdir(output_path) # returns list
if len(contents):
    print(colored("Output directory is not empty, below are it's contents:", 'blue'))
    print(contents)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()

# show what is in input (files AND directories)
path = 'input'
contents = os.listdir(path)  # returns list
if not len(contents):
    print(colored("Input directory is empty. Press 'y' once you fill it. Press 'n' to terminate program.", 'blue'))
    choice = input()
    if choice != 'y':
        exit()
else:
    print(colored("Below are contents of input folder:", 'blue'))
    for content in contents:
        print(content)
    print(colored("Continue or exit? (y/n)", 'blue'))
    choice = input()
    if choice != 'y':
        exit()
print(colored("Print parameters:", 'blue'))
print(colored("1    Apply balancing weights? (y/n)", 'blue'))
print(colored("2    Apply automatic scaling? (y/n)", 'blue'))
parameters = input()
if parameters[-1] != 'y':
    print(colored("Print vmin and vmax", 'blue'))
    parameters = parameters + ' ' + input()

# create temp.txt filling its lines with parameters
onlyfiles = ['input/' + f + ' ' + parameters for f in listdir(path) if isfile(join(path, f))]
f = open("temp.txt", "w")
for i in onlyfiles:
    f.write(i + '\n')
f.close()
