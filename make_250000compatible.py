import pandas as pd

infilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/conserved_bins.txt'
outfilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/conserved_bins_compatible.csv'

conserved_bins = pd.read_csv(infilepath)
conserved_bins_compatible = pd.DataFrame(columns = ['conservation', 'compartment']) # see newest scripts for how to call it

for i in conserved_bins.index:
    conserved_bins_compatible.loc[conserved_bins_compatible.shape[0]] = [conserved_bins['conservation'][i], conserved_bins['compartment'][i]]
    conserved_bins_compatible.loc[conserved_bins_compatible.shape[0]] = [conserved_bins['conservation'][i], conserved_bins['compartment'][i]]

conserved_bins_compatible.to_csv(outfilepath, index=False, index_label=False, header=False)

