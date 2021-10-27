# get list with lines
with open('input.txt') as f:
    lines = f.readlines()

whitelist = ['1. ', '2. ', '3. ', '4.']

result = []

# make list with selected lines
for line in lines:
    for i in whitelist:
        if line.find(i) > -1:
            result.append(line)

# delete markers from lines
for line in result:
    for i in whitelist:
        if line.find(i) > -1:
            idOfLine = result.index(line)
            newLine = line[(line.find(i)) + 3:]
            result.remove(line)
            result.insert(idOfLine, newLine)

# make text file filling it with newly made lines
with open('output.txt', 'w') as f:
    for line in result:
        f.write("%s" % line)

print('job finished')
