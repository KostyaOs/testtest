import os

files = os.listdir('input')

for file in files:
    print(file)
    newLines = []
    with open('input/' + file, "rt", encoding="utf-8") as f:
        lines = f.readlines()
        newLines.append(lines[0])
        newLines.append(lines[1][:lines[1].find(';')] + '\n')
        newLines.append(lines[2][:lines[1].find(';')])
    with open('output/' + file, "wt", encoding="utf-8") as f:
        for line in newLines:
            f.write("%s" % line)

