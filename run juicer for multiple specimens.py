# below is required folder structure
# juicer-top
#     references
#     restriction_sites
#     scripts
#     work
#         fastq
import os

path = '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top'  # '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top'
genome_id = 'hg19'  # 'hg19'
enzyme = 'MboI'  # 'MboI'
chrom_sizes = 'hg19.chrom.sizes'  # 'hg19.chrom.sizes'
sites_txt = 'hg19_MboI.txt'  # 'hg19_MboI.txt'
fasta = 'Homo_sapiens_assembly19.fasta'  # 'Homo_sapiens_assembly19.fasta'

dir_contents = os.listdir(path + '/work')
for specimen_name in dir_contents:
    command = path + '/scripts/juicer.sh' + ' -g ' + genome_id + ' -d ' + path + '/work' + '/' + specimen_name + ' -s ' + enzyme + ' -p ' + path + \
         '/references/' + chrom_sizes + ' -y ' + path + '/restriction_sites/' + sites_txt + ' -z ' + path + \
         '/references/' + fasta + ' -D ' + path + ' -a ' + specimen_name
    #os.system(command)
    print(command)
    print()

