import os
import shutil


def spec_name(rootpath):
    rootpath = rootpath[rootpath.find('\\') + 1:]
    return rootpath


# define source directory
inshareddirpath = 'D:/pit/forPre'

# define target directory
outshareddirpath = 'D:/pit/juicerResult'



# for file in source directory
    # send it to target subdir
    # get name of specimen
for root, dirs, files in os.walk(inshareddirpath, followlinks=True):
    for f in files:
        specname = spec_name(root)
        inpath = root + '/' + f
        outpath = outshareddirpath + '/' + specname + '/aligned/' + f
        shutil.move(inpath, outpath)
        print('finished with file', f)
print('finished them all')

