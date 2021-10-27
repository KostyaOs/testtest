from os import listdir
from os.path import isfile, join

# print('input absolute path to the folder to be observed')
# mypath = input()
mypath = '/mnt/storage/home/knostroverkhii/=workspace/input'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

f = open("temp.txt","w+")
for i in onlyfiles:
     f.write(i + '\n')
f.close()