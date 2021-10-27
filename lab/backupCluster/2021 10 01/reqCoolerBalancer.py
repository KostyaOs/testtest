from termcolor import colored
import os


def mainfunc(pathF):
    command = 'cooler balance --force ' + pathF
    os.system(command)


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
    for filename in contents:
        print(filename)
    print(colored("Continue (Enter) or exit (Ctrl + C)?", 'blue'))
    input()


filenames = os.listdir(input_path)  # make list of files in input folder
for filename in filenames:
    if filename.endswith(".cool"):  # if file is '.cool' file
        path = input_path + "/" + filename  # path to input file
        mainfunc(path)
        print(colored("file has been processed", 'blue'))
