import cooler
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

name_of_cooler = '/mnt/storage/home/knostroverkhii/workspace/input/3471-G.cool'
clr = cooler.Cooler(name_of_cooler)
# clr = cooler.Cooler('XXtrans.cool')
chrom_sizes_bins = (clr.chromsizes // clr.binsize).tolist()
chrom_size_matrix = [[0] * 24 for i in range(24)]
for i in range(24):
    for j in range(24):
        chrom_size_matrix[i][j] = chrom_sizes_bins[i] * chrom_sizes_bins[j]
df_chrom_size_matrix = pd.DataFrame(data=chrom_size_matrix)
mtx = clr.matrix(balance=True, as_pixels=True, join=True)
mtx = pd.DataFrame(data=clr.matrix(balance=True, as_pixels=True, join=True)[:, :])
mtx['balanced'] = mtx['balanced'].fillna(value=0)
mtx = mtx.drop(columns=['start1', 'end1', 'start2', 'end2', 'count'])
trans_contacts = mtx[mtx['chrom1'] != mtx['chrom2']]
sum = trans_contacts.groupby(by=['chrom1', 'chrom2']).sum()
sum.to_csv(name_of_cooler + 'README.csv')
sum = pd.read_csv(name_of_cooler + 'README.csv')
# sum = pd.read_csv('XXtrans.cool' + '.csv')
new_indexes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
               '19', '20', '21', '22', 'X', 'Y']
sum = sum.pivot(index='chrom1', columns='chrom2')
sum.columns = sum.index
sum = sum.where(sum != 0, sum.T)
sum = sum.reindex(index=new_indexes, columns=new_indexes)
sum = pd.DataFrame(sum.values / df_chrom_size_matrix.values, columns=new_indexes, index=new_indexes)
sum.to_csv(name_of_cooler + 'SECOND.csv')
plt.cla()
fig = sns.heatmap(data=sum, cmap='Reds')
fig.figure.savefig(name_of_cooler + '.png')
