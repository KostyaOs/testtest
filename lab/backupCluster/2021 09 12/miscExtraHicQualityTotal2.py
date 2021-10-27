import sys


file = sys.argv[1]
with open(file, "rt", encoding="utf-8") as f:
    lines = f.readlines()
total = len(lines)

specimen = sys.argv[2]
with open('/mnt/storage/home/knostroverkhii/workspace/output/' + specimen + '.txt', 'wt') as data_file:
    data_file.write(f'{total}')
