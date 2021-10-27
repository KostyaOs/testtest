# get list with lines
with open('input.txt') as f:
    lines = f.readlines()

# delete '\n'
for line in lines:
    if line != "\n":
        idOfLine = lines.index(line)
        lines.remove(line)
        newLine = line[:(line.find('\n'))]
        lines.insert(idOfLine, newLine)

# make text file filling it with newly made lines
with open('output.txt', 'w') as f:
    for line in lines:
        f.write("%s\n" % line)

print('job finished')
