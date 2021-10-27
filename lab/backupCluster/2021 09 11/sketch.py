command = 'echo "python reqCisTransHicPairs.py" | qsub -l select=1:ncpus=4:mem=30gb,walltime=1:0:0'
    os.system(command)