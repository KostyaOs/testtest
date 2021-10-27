# get list with lines
with open('input.txt') as f:
    lines = f.readlines()

result = []

for line in lines:
    if line.count('`') == 0:
        result.append(line)

# make text file filling it with newly made lines
with open('output.txt', 'w') as f:
    for line in result:
        f.write("%s" % line)

print('job finished')
