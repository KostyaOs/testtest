import os
import shutil


print('print path to folder in which processed specimens folders are located')
path = '/mnt/scratch/ws/knostroverkhii/202108071238ws1/dataToDownload'
print('---')

listOfSpecimens = os.listdir(path)
listOfSpecimens.sort()
for specimen in listOfSpecimens:
    pathToSpecimen = path + '/' + specimen
    shutil.rmtree(pathToSpecimen + '/splits')
    os.remove(pathToSpecimen + '/aligned/' + 'abnormal.sam')
    os.remove(pathToSpecimen + '/aligned/' + 'collisions.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'merged_sort.txt.gz')
    os.remove(pathToSpecimen + '/aligned/' + 'opt_dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'stats_dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'unmapped.sam')


print('job finished')
