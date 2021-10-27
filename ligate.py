import pandas as pd

chroms = []
for i in range(1,22):
    chroms.append(str(i + 1))
chroms.append('X')

outfilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/merged_merged/nodups_for_female_chorion_none/output/concatvectors_res500000.txt'
infilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/merged_merged/nodups_for_female_chorion_none/output/finalvector_res500000_chrom1.txt'
concatvectors = pd.read_csv(infilepath,names='column')
for i in chroms:
    infilepath = '/mnt/scratch/ws/knostroverkhii/202111161241B/merged_merged/nodups_for_female_chorion_none/output/finalvector_res500000_chrom' + i + '.txt'
    df = pd.read_csv(infilepath, names='column')
    concatvectors = pd.concat(concatvectors, df)

concatvectors.to_csv(outfilepath, index=False, index_label=False, header=False)

