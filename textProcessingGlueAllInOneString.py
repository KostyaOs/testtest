# get list with lines
with open('input.txt') as f:
    lines = f.readlines()

temp = ''

# glue lines, remove '\n'
for line in lines:
    line = line.replace('\n', '')
    temp += line

# Make list from elements between '.'. Input.txt should end with '.'
#while temp.count('.') != 0:
result = list(temp.split('.'))

print(result)
# make text file filling it with newly made lines
with open('output.txt', 'w') as f:
    for line in result:
        f.write("%s\n" % line)

print('job finished')
