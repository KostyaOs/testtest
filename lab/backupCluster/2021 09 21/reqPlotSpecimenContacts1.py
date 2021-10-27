import os

specimensDir = '/mnt/storage/home/knostroverkhii/workspace/input'
specimens = os.listdir(specimensDir)
for specimen in specimens:
    command = 'echo "source /mnt/storage/home/knostroverkhii/anaconda3/envs/squareMaps/bin/activate; python workspace/reqPlotSpecimenContacts2.py ' + specimensDir + ' ' + specimen + '" | qsub -l select=1:ncpus=1:mem=6gb,walltime=1:0:0'
    os.system(command)
