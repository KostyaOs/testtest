import os
import shutil

files = os.listdir('targetDir')

for file in files:
    if file[0] == 'm':
        shutil.move('targetDir/' + file, 'targetDir/' + file[1:])


