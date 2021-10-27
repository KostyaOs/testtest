import os
import shutil


print('print path to folder in which new folders should be made')
pathGeneral = input()
print()
print('print names of new folders, separate them using space button')
foldersList = list(map(str, input().split()))

for i in foldersList:
    pathSpecific = pathGeneral + '/' + i
    os.mkdir(pathSpecific)

print('job finished')
