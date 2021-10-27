# below is required folder structure
# juicer-top
#     references
#     restriction_sites
#     scripts
#     work
#         fastq

path = '/mnt/storage/home/knostroverkhii/home'  # '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top'
genome_id = 'hg19'  # 'hg19'
enzyme = 'MboI'  # 'MboI'
chrom_sizes = 'hg19.chrom.sizes'  # 'hg19.chrom.sizes'
sites_txt = 'hg19_MboI.txt'  # 'hg19_MboI.txt'
fasta = 'Homo_sapiens_assembly19.fasta'  # 'Homo_sapiens_assembly19.fasta'
queue_general = 'bl2x220g7q'  # 'bl2x220g7q'
queue_long = 'bl2x220g7q'  # 'bl2x220g7q'
queue_V = 'teslaq' # 'teslaq'

output = path + '/scripts/juicer.sh' + ' -g ' + genome_id + ' -d ' + path + '/work' + ' -s ' + enzyme + ' -p ' + path + \
         '/references/' + chrom_sizes + ' -y ' + path + '/restriction_sites/' + sites_txt + ' -z ' + path + \
         '/references/' + fasta + ' -D ' + path + ' -q ' + queue_general + ' -l ' + queue_long + ' -V ' + queue_V + ' -x'
print(output)
