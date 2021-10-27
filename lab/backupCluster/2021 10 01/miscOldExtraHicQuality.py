import os


def str1(line):
    pos = line.find(' ')
    return line[:pos]


def str2(line):
    pos = line.find(' ')
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos2 = line.find(' ', pos + 1)
    pos += 1
    return line[pos:pos2]


def chr1(line):
    pos = line.find(' ')
    pos2 = line.find(' ', pos + 1)
    pos += 1
    return line[pos:pos2]


def chr2(line):
    pos = line.find(' ')
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos2 = line.find(' ', pos + 1)
    pos += 1
    return line[pos:pos2]

specimensDir = '/mnt/scratch/ws/knostroverkhii/202109210904A/forPreSource'
specimens = os.listdir(specimensDir)
files = []
for specimen in specimens:
    files.append(specimensDir + '/' + specimen + '/merged_nodups.txt')

DErow = []
transRow = []
cisRow = []
for file in files:
    with open(file, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    total = len(lines)
    ff = 0
    fft = 0
    rr = 0
    rrt = 0
    for string in lines:
        if str1(string) == '0' and str2(string) == '0':
            ff += 1
            if chr1(string) != chr2(string):
                fft += 1
        elif str1(string) != '0' and str2(string) != '0':
            rr += 1
            if chr1(string) != chr2(string):
                rrt += 1
    DE = total - 2 * (ff + rr)
    trans = (fft + rrt) / (ff + rr)
    cis = 1 - trans
    DErow.append(DE)
    transRow.append(trans)
    cisRow.append(cis)
    print(file)
    print(DE)
    print(cis)
    print(trans)

with open('/mnt/storage/home/knostroverkhii/workspace/output/Extra.csv', 'wt') as data_file:
    data_file.write(';')
    for specimen in specimens:
        data_file.write(f'{specimen};')
    data_file.write('\n')
    data_file.write('DE_pairs;')
    for DE in DErow:
        data_file.write(f'{DE};')
    data_file.write('\n')
    data_file.write('Cis_Hi-C_pairs;')
    for cis in cisRow:
        data_file.write(f'{cis};')
    data_file.write('\n')
    data_file.write('Trans_Hi-C_pairs;')
    for trans in transRow:
        data_file.write(f'{trans};')
    data_file.write('\n')
