import os
from shutil import copyfile

sharedPath = 'D:/scratch/symbols/roots'

targetList = []
signal = 'none'
while signal != '0':
    signal = input()
    if signal != '' or '0':
        targetList.append(signal)

listOfFiles = os.listdir(sharedPath)
listOfFiles.sort()
for i in listOfFiles:
    sourcePath = sharedPath + '/' + i
    targetPath = sharedPath + '/' + targetList[listOfFiles.index(i)] + '.png'
    os.rename(sourcePath, targetPath)

print('job finished')
