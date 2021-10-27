import cooler
import sys
import pandas as pd
from termcolor import colored

c = cooler.Cooler(sys.argv[1])
mtx = c.matrix(balance=True, as_pixels=True, join=True)[:]
mtx['balanced'] = mtx['balanced'].fillna(value=0)
print(mtx)

mean_genome = mtx['balanced'].mean()
std_genome = mtx['balanced'].std()
print(colored('mean genome = ', 'yellow'))
print(colored(str(mean_genome), 'yellow'))
print(colored('std genome = ', 'yellow'))
print(colored(str(std_genome), 'yellow'))
print()

for i in range(22):
    cis_chrI = mtx['balanced'][mtx['chrom1'] == 'chr' + str(i + 1)][mtx['chrom2'] == 'chr' + str(i + 1)]
    mean_cis_chrI = cis_chrI.mean()
    std_cis_chrI = cis_chrI.std()
    print(colored('mean cis_chr' + str(i + 1) + ' = ', 'yellow'))
    print(colored(str(mean_cis_chrI), 'yellow'))
    print(colored('std cis_chr' + str(i + 1) + ' = ', 'yellow'))
    print(colored(str(std_cis_chrI), 'yellow'))
    print()
for i in ('X', 'Y'):
    cis_chrI = mtx['balanced'][mtx['chrom1'] == 'chr' + i][mtx['chrom2'] == 'chr' + i]
    mean_cis_chrI = cis_chrI.mean()
    std_cis_chrI = cis_chrI.std()
    print(colored('mean cis_chr' + i + ' = ', 'yellow'))
    print(colored(str(mean_cis_chrI), 'yellow'))
    print(colored('std cis_chr' + i + ' = ', 'yellow'))
    print(colored(str(std_cis_chrI), 'yellow'))
    print()

print(colored("SCV: 'Job finished!'", 'green'))