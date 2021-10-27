import cooler
import sys
from termcolor import colored

clr = cooler.Cooler(sys.argv[1])  # read cool file
print('binsize is ', clr.binsize)

print(colored('finished', 'green'))