import pandas as pd

filepath13 ='/mnt/scratch/ws/knostroverkhii/202111161241B/merged_merged/nodups_for_female_chorion_13+/output/concatvectors_res500000.txt'
filepathnone ='/mnt/scratch/ws/knostroverkhii/202111161241B/merged_merged/nodups_for_female_chorion_none/output/concatvectors_res500000.txt'
outfilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/conserved_bins.csv'

df13 = pd.read_csv(filepath13,names='column')
dfnone = pd.read_csv(filepathnone,names='column')

df13['column'] /= abs(df13['column'])
dfnone['column'] /= abs(dfnone['column'])
conserved_bins = pd.DataFrame(columns = ['conservation', 'compartment']) # see newest scripts for how to call it

for i in df13.index:
    if df13['column'][i] == dfnone['column'][i]:
        conserved_bins.loc[conserved_bins.shape[0]] = [True, df13['column'][i]]
    else:
        conserved_bins.loc[conserved_bins.shape[0]] = [False, False]

conserved_bins.to_csv(outfilepath, index=False, index_label=False)


