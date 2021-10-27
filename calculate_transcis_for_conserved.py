import cooler
import pandas as pd

infilepath_bins = '/mnt/scratch/ws/knostroverkhii/202111161241B/conserved_bins_compatible.csv'
infilepath_cooler = # TODO fill

clr = cooler.Cooler(infilepath_cooler)

# calculate for compartment A
conserved_bins = pd.read_csv(infilepath_bins)
conserved_bins = conserved_bins[conserved_bins['conservation'] == True]
conserved_bins = conserved_bins[conserved_bins['compartment'] == 1]
conserved_bins = list(conserved_bins.index.values) # get list with bin ids # TODO check that indexation is the same in cooler and my conserved_bins.xtx

# calculate trans sum
pixels = clr.pixels()[:]  # extract pixels data
pixels = pixels[pixels['bin1_id'].isin(conserved_bins)]
pixels = pixels[pixels['bin2_id'].isin(conserved_bins)]
trans_sum = pixels['balanced'].sum()

# calculate cis sum
pixels = clr.pixels()[:]  # extract pixels data
pixels = pixels[pixels['bin1_id'].isin(conserved_bins)]
pixels = pixels[pixels['bin1_id'] == pixels['bin2_id']] # TODO check if it works
cis_sum = pixels['balanced'].sum()

transcis = trans_sum / cis_sum
print('transcis for compartment A is', transcis)

# calculate for compartment B
conserved_bins = pd.read_csv(infilepath_bins)
conserved_bins = conserved_bins[conserved_bins['conservation'] == True]
conserved_bins = conserved_bins[conserved_bins['compartment'] == -1]
conserved_bins = list(conserved_bins.index.values) # get list with bin ids # TODO check that indexation is the same in cooler and my conserved_bins.xtx

# calculate trans sum
pixels = clr.pixels()[:]  # extract pixels data
pixels = pixels[pixels['bin1_id'].isin(conserved_bins)]
pixels = pixels[pixels['bin2_id'].isin(conserved_bins)]
trans_sum = pixels['balanced'].sum()

# calculate cis sum
pixels = clr.pixels()[:]  # extract pixels data
pixels = pixels[pixels['bin1_id'].isin(conserved_bins)]
pixels = pixels[pixels['bin1_id'] == pixels['bin2_id']] # TODO check if it works
cis_sum = pixels['balanced'].sum()

transcis = trans_sum / cis_sum
print('transcis for compartment B is', transcis)

