import os
import shutil

specimens = os.listdir('input')
print('check that you have output folder in the same place where script is located')
print('if you do - press "y" to continue')
if input() != 'y':
    print("you typed not 'y' - aborting script")
    exit()
for specimen in specimens:
    sourcePathDups = 'input/' + specimen + '/aligned/merged_nodups.txt'
    sourcePathStat = 'input/' + specimen + '/aligned/inter_30.txt'
    sourcePathHist = 'input/' + specimen + '/aligned/inter_30_hists.m'
    targetPath = 'output/' + specimen
    os.makedirs(targetPath)
    shutil.move(sourcePathDups, targetPath)
    shutil.move(sourcePathStat, targetPath)
    shutil.move(sourcePathHist, targetPath)
    print('finished moving hic file of specimen', specimen)