# below is required folder structure
# juicer-top
#     references
#     restriction_sites
#     scripts
#     work
#         fastq
import os

specimensDataPath = '/mnt/scratch/ws/knostroverkhii/202111161241B/specimensData'
pathToOther = '/mnt/storage/home/knostroverkhii/home'  # '/media/k/B4AC8B7FAC8B3ABE/=workspace/juicer-top'
genome_id = 'hg19'  # 'hg19'
enzyme = 'DpnII'  # 'MboI'
chrom_sizes = 'hg19.chrom.sizes'  # 'hg19.chrom.sizes'
sites_txt = 'hg19_DpnII.txt'  # 'hg19_MboI.txt'
fasta = 'Homo_sapiens_assembly19.fasta'  # 'Homo_sapiens_assembly19.fasta'
queue_general = 'bl2x220g7q'  # 'bl2x220g7q'
queue_long = 'bl2x220g7q'  # 'bl2x220g7q'
queue_V = 'teslaq' # 'teslaq'
#stage = '' # for repeated run

dir_contents = os.listdir(specimensDataPath)
for specimen_name in dir_contents:
    # synthesize command
    command = pathToOther + '/scripts/juicer.sh' + ' -g ' + genome_id + ' -d ' + specimensDataPath + '/' + specimen_name + ' -s ' + enzyme + ' -p ' + pathToOther + \
         '/references/' + chrom_sizes + ' -y ' + pathToOther + '/restriction_sites/' + sites_txt + ' -z ' + pathToOther + \
         '/references/' + fasta + ' -D ' + pathToOther + ' -a ' + specimen_name + ' -q ' + queue_general + ' -l ' + queue_long + ' -V ' + queue_V + ' -x'
    # send command
    os.system(command)
    #print(command)
    print("-----------------------------------")
