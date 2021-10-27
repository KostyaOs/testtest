import os
import shutil

pathToScratch = '/mnt/scratch/ws/knostroverkhii/202109210904A'
pathToDirForDirsWithLogs = pathToScratch + '/dirForDirsWithLogs'

# check dirForDirsWithLogs
print('###')
print('going to check dirForDirsWithLogs folder, which will be used as directory for directories with logs')
print('###')

if os.path.isdir(pathToDirForDirsWithLogs):
    print('dirForDirsWithLogs folder already exists, empty it, then type "y" to proceed')
    print('###')
    if input() != "y":
        exit()
    print('###')
else:
    os.mkdir(pathToDirForDirsWithLogs)

print('type date without spaces, it will be attached to name of each folder')
print('###')
date = input()

# move logs
print('going to move logs to dirForDirsWithLogs folder')
print('###')

pathToSpecimensData = pathToScratch + '/specimensData'
listOfSpecimens = os.listdir(pathToSpecimensData)
listOfSpecimens.sort()

for specimen in listOfSpecimens:
    sourcePath = pathToSpecimensData + '/' + specimen + '/logs'
    targetPath = pathToDirForDirsWithLogs + '/' + specimen + '_' + date
    os.mkdir(targetPath)
    shutil.move(sourcePath, targetPath)

print('finished moving to dirForDirsWithLogs')
print('###')

# delete all except fastq
print('going to delete useless files')
print('###')

for specimen in listOfSpecimens:
    pathToSpecimen = pathToSpecimensData + '/' + specimen
    listOfTrash = os.listdir(pathToSpecimen)
    listOfTrash.remove('fastq')
    listOfTrash.sort()
    for trash in listOfTrash:
        shutil.rmtree(pathToSpecimen + '/' + trash)

print('finished deleting')
print('###')
