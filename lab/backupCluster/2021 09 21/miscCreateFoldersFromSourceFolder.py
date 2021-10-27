import os
import shutil


print('print path to folder in which new folders should be made')
pathTarget = input()
print('---')
print('print path to source folder from which names of folders should be copied')
pathSource = input()
print('---')

foldersList = os.listdir(pathSource)
for folderName in foldersList:
    pathSpecific = pathTarget + '/' + folderName
    os.mkdir(pathSpecific)

print('job finished')
