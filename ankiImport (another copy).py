# get list with lines
with open('readme.txt') as f:
    lines = f.readlines()

# modification for cycle to work right
lines = lines + ['\n', '\n', '\n']

# delete '\n'
for line in lines:
    if line != "\n":
        idOfLine = lines.index(line)
        lines.remove(line)
        newLine = line[:(line.find('\n'))]
        lines.insert(idOfLine, newLine)

# get list with numbers of lines where question starts
idsOfStartingLines = [0]
for line in lines:
    idOfCurrentLine = lines.index(line)
    prior1st = idOfCurrentLine - 1
    prior2nd = idOfCurrentLine - 2
    prior3rd = idOfCurrentLine - 3
    if idOfCurrentLine > 3:
        if lines[prior1st] == "\n" and lines[prior2nd] == "\n" and lines[prior3rd] == "\n":
            idsOfStartingLines.append(lines.index(line))

listForNewFile = []
for number in idsOfStartingLines:
    listForNewFile.append(lines[number])
    while lines[number + 2] != '\n':
        listForNewFile[-1] = listForNewFile[-1] + '<br><br>' + lines[number + 2]
        number = number + 2
    listForNewFile[-1] = listForNewFile[-1] + ';'
    number = number + 3
    listForNewFile[-1] = listForNewFile[-1] + lines[number]
    while lines[number + 2] != '\n':
        listForNewFile[-1] = listForNewFile[-1] + '<br><br>' + lines[number + 2]
        number = number + 2
    listForNewFile[-1] = listForNewFile[-1] + ';' + 'биология биология_иммунология'

for line in listForNewFile:
    print(line)

with open('your_file.txt', 'w') as f:
    for line in listForNewFile:
        f.write("%s\n" % line)

print('job finished')
