import os

specimensDir = '/mnt/scratch/ws/knostroverkhii/202109210904A/forPreSource'
specimens = os.listdir(specimensDir)
for specimen in specimens:
    file = specimensDir + '/' + specimen + '/merged_nodups.txt'
    command = 'echo "python workspace/miscExtraHicQualityTotal2.py ' + file + ' ' + specimen + '" | qsub -l select=1:ncpus=1:mem=24gb,walltime=3:0:0'
    os.system(command)
