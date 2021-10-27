import cooler
from termcolor import colored

input_uris = os.listdir('input')
print('check that you have output folder in the same place where script is located')
print('if you do - press "y" to continue')
if input() != 'y':
    print("you typed not 'y' - aborting script")
    exit()

print('print name of output file, without extension')
output_uri = 'output/' + input() + '.cool'

mergebuf = cooler.Cooler('input/' + input_uris[0]).info['nnz'] # cooler.Cooler.binsize('XX.cool') # number of pixels, i.e. number of rows in matrix table

cooler.merge_coolers(output_uri, input_uris, mergebuf)

print(colored("SCV: 'Job finished!'", 'green'))