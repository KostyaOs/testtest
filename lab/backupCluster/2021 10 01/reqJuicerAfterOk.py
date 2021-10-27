import os
import shutil


pathToScratch = '/mnt/scratch/ws/knostroverkhii/202111161241B'
pathToTemp = pathToScratch + '/temp'

# check temp
print('###')
print('going to check temp folder')
print('###')

if os.path.isdir(pathToTemp):
    print('temp folder already exists, empty it, then type "y" to proceed')
    print('###')
    if input() != "y":
        exit()
    print('###')
else:
    os.mkdir(pathToTemp)

# move to temp
print('going to move specimens to temp folder')
print('###')

pathToSpecimensData = pathToScratch + '/specimensData'
listOfSpecimens = os.listdir(pathToSpecimensData)
listOfSpecimens.sort()

for specimen in listOfSpecimens:
    pathToSpecimen = pathToSpecimensData + '/' + specimen
    shutil.move(pathToSpecimen, pathToTemp)

print('finished moving to temp')
print('###')


# move fastq
print('going to move fastq files back to storage')
print('###')

pathToProcessedFastq = '/mnt/storage/home/knostroverkhii/=results/aneuploidyFastq'

for specimen in listOfSpecimens:
    sourcePath = pathToTemp + '/' + specimen + '/fastq'
    targetPath = pathToProcessedFastq + '/' + specimen
    os.mkdir(targetPath)
    shutil.move(sourcePath, targetPath)

# delete
print('going to delete useless files')
print('###')

for specimen in listOfSpecimens:
    pathToSpecimen = pathToTemp + '/' + specimen
    shutil.rmtree(pathToSpecimen + '/splits')
    os.remove(pathToSpecimen + '/aligned/' + 'abnormal.sam')
    os.remove(pathToSpecimen + '/aligned/' + 'collisions.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'merged_sort.txt.gz')
    os.remove(pathToSpecimen + '/aligned/' + 'opt_dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'stats_dups.txt')
    os.remove(pathToSpecimen + '/aligned/' + 'unmapped.sam')

# ask to check
print('finished deleting')
#print('###')
#print('check that all was done properly, type "y" to proceed - going to make archive then')
#print('###')
#if input() != "y":
#   exit()
#print('###')
#print('type name of archive to be created, without extension')

# archive result
#pathToArchive = pathToScratch + '/' + input() + '.tar.gz'
#command = 'tar -czvf ' + pathToArchive + ' ' + pathToTemp
#os.system(command)

print('job finished')
print('###')
