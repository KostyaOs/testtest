import cooler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from termcolor import colored


def cut_extension(path_func):
    return path_func[:path_func.find('.')]


table_path = '/mnt/storage/home/knostroverkhii/workspace/input/heat_plotter_test.csv'
mtx = pd.read_csv(table_path)
mtx = mtx[mtx['balanced'].notna()]
print(mtx)

# names of chromosomes in new_indexes should be the same as in .cool file; otherwise table values get lost
new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
               '19', '20', '21', '22', 'X', 'Y']
# print('enter gender of specimen: 0 for female, <anything else> for male')
# if input() == 0:
#   new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
#                 '19', '20', '21', '22', 'X']
# else:
#   new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
#                 '19', '20', '21', '22', 'X', 'Y']
mtx = mtx.pivot(index='chrom1', columns='chrom2')

mtx.columns = mtx.index
mtx = mtx.where(mtx != 0, mtx.T)
print(mtx)

mtx = mtx.reindex(index=new_indexes, columns=new_indexes)
print(mtx)

mtx = pd.DataFrame(mtx.values, columns=new_indexes, index=new_indexes)
mtx.to_csv(cut_extension(table_path) + '_after_plotting.csv')  # TODO check if it is redundant line
plt.cla()
print(mtx)
fig = sns.heatmap(data=mtx, cmap='Reds')

output_path = cut_extension(table_path) + '_after_plotting.png'
fig.figure.savefig(output_path)
