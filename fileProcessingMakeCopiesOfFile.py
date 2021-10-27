import os
from shutil import copyfile

mode = int(input())  # chose mode of work

if mode == 1:  # make multiple copies of one file
    sharedPath = 'D:/scratch/symbols/nonprefixes-words'
    sourcePath = sharedPath + '/vessel.png'
    for i in range(16):
        targetPath = sharedPath + '/vessel' + str(i) + '.png'
        copyfile(sourcePath, targetPath)
elif mode == 2:  # make copies of files from different folder and store them in one folder
    specimens = os.listdir('input')
    print('check that you have output folder in the same place where script is located')
    print('if you do - press "y" to continue')
    if input() != 'y':
        print("you typed not 'y' - aborting script")
        exit()
    for specimen in specimens:
        sourcePath = 'input/' + specimen + '/aligned/inter_30.hic'
        targetPath = 'output/' + specimen + '.hic'
        copyfile(sourcePath, targetPath)
        print('finished copying hic file of specimen', specimen)