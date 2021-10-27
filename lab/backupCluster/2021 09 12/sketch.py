import cooler
import os

files = os.listdir('input')

for file in files:
    clr = cooler.Cooler('input/' + file)
    print(clr.chromnames)
