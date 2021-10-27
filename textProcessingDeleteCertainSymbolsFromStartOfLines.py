# get list with lines
with open('input.txt') as f:
    lines = f.readlines()

blacklist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '№', ' ', '.']

result = []

for line in lines:
    while blacklist.count(line[0]) > 0:
        line = line[1:]
    result.append(line)

# make text file filling it with newly made lines
with open('output.txt', 'w') as f:
    for line in result:
        f.write("%s" % line)

print('job finished')
