import os
from shutil import copyfile

# check that folder is empty, ask to fill it
importFolder = 'D:/storage/pycharmProjects/project1/import'
listForImportFolder = os.listdir(importFolder)

if len(listForImportFolder):
    print('import folder already contains files, if those files are the ones you need AND THEY ARE ".PNG", type "y" to proceed')
    print('###')
    if input() != "y":
        exit()
    print('###')
else:
    print('Import folder is empty. Fill it, then type "y" to proceed')
    print('###')
    if input() != "y":
        exit()
    print('###')

listForImportFolder.sort()

print('type date, below is example')
print('20210808')
date = input()

for file in listForImportFolder:
    if file.endswith('.png'):
        sourcePath = importFolder + '/' + file
        targetPath = importFolder + '/' + date + file
        os.rename(sourcePath, targetPath)
        sourcePath = targetPath
        targetPath = 'C:/Users/k/AppData/Roaming/Anki2/User 1/collection.media/' + date + file
        copyfile(sourcePath, targetPath)

print('job finished')
