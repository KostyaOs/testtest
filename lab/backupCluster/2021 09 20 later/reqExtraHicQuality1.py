import os

specimensDir = '/mnt/scratch/ws/knostroverkhii/202111161241B/forPreSource'
specimens = os.listdir(specimensDir)
for specimen in specimens:
    file = specimensDir + '/' + specimen + '/merged_nodups.txt'
    command = 'echo "python workspace/reqExtraHicQuality2.py ' + file + ' ' + specimen + '" | qsub -l select=1:ncpus=1:mem=24gb,walltime=3:0:0'
    os.system(command)
