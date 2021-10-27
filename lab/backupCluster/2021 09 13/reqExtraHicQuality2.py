import sys


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


def frag1(line):
    pos = line.find(' ')
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos2 = line.find(' ', pos + 1)
    pos += 1
    return line[pos:pos2]


def frag2(line):
    pos = line.find(' ')
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos = line.find(' ', pos + 1)
    pos2 = line.find(' ', pos + 1)
    pos += 1
    return line[pos:pos2]


choice = 0

file = sys.argv[1]
with open(file, "rt", encoding="utf-8") as f:
    lines = f.readlines()
total = len(lines)
ff = 0
rr = 0
fr = 0
rf = 0
intra = 0
intraFR = 0
for string in lines:
    if frag1(string) == frag2(string):
        intra += 1
    if str1(string) == '0' and str2(string) == '0':
        ff += 1
    elif str1(string) != '0' and str2(string) != '0':
        rr += 1
    elif str1(string) == '0' and str2(string) != '0':
        fr += 1
        if frag1(string) == frag2(string):
            intraFR += 1
    elif str1(string) != '0' and str2(string) == '0':
        rf += 1

DEinIntra = intraFR / intra
realDE = (fr - 0.5 * (ff + rr)) / total
rings = (rf - 0.5 * (ff + rr)) / total

specimen = sys.argv[2]
with open('/mnt/storage/home/knostroverkhii/workspace/output/' + specimen + '.txt', 'wt') as data_file:
    data_file.write(f'{DEinIntra}')
    data_file.write('\n')
    data_file.write(f'{realDE}')
    data_file.write('\n')
    data_file.write(f'{rings}')

if choice == 'DE, total,DEfrac, cis, trans':
    file = sys.argv[1]
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
    DEfrac = DE / total
    trans = (fft + rrt) / (ff + rr)
    cis = 1 - trans

    specimen = sys.argv[2]
    with open('/mnt/storage/home/knostroverkhii/workspace/output/' + specimen + '.txt', 'wt') as data_file:
        data_file.write(f'{DE}')
        data_file.write('\n')
        data_file.write(f'{total}')
        data_file.write('\n')
        data_file.write(f'{DEfrac}')
        data_file.write('\n')
        data_file.write(f'{cis}')
        data_file.write('\n')
        data_file.write(f'{trans}')
