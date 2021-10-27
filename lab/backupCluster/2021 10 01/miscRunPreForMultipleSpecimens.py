import os

source = '/mnt/scratch/ws/knostroverkhii/202109210904A/forPreSource'
genomeID = '/mnt/storage/home/knostroverkhii/home/references/hg19.chrom.sizes'
destination = '/mnt/scratch/ws/knostroverkhii/202109210904A/forPreDestination'
juiceboxTools = '/mnt/storage/home/knostroverkhii/home/juicer/juicer_tools/juicer_tools_1.19.02.jar '
#enzyme = '/mnt/storage/home/knostroverkhii/home/restriction_sites/hg19_DpnII.txt'

specimens = os.listdir(source)
for specimen in specimens:
    # synthesize command
    infile = source + '/' + specimen + '/merged_nodups.txt'
    outfile = destination + '/' + specimen + '.hic'
    statistics = source + '/' + specimen + '/inter_30.txt'
    graphs = source + '/' + specimen + '/inter_30_hists.m'
    command = 'echo "module load jre/1.8.0;java -Xmx2g -jar ' + juiceboxTools + ' pre -q 30 -s ' + statistics + ' -g ' + graphs + \
              ' ' + infile + ' ' + outfile + ' ' + genomeID + '" | qsub -l select=1:ncpus=4:mem=20gb,walltime=8:0:0'
    #command = 'qsub -l select=1:ncpus=4:mem=16gb,walltime=10:0:0 -- module load jre/1.8.0;java -Xmx2g -jar ' + juiceboxTools + ' pre -q 30 -f ' + enzyme + ' -s ' + statistics + ' -g ' + graphs + \
              #' ' + infile + ' ' + outfile + ' ' + genomeID
    #command = 'java -Xmx2g -jar ' + juiceboxTools + ' pre -q 30 -f ' + enzyme + ' -s ' + statistics + ' -g ' + graphs + \
     #         ' ' + infile + ' ' + outfile + ' ' + genomeID
    # send command
    os.system(command)
    #print(command)
    print("-----------------------------------")
