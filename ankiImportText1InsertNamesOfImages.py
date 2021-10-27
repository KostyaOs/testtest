print("Check formatting of input.txt if you haven't. '*' should be after image number. Type 'y' to proceed")
if input() != 'y':
    print("you typed not 'y' - aborting script")
    exit()

# get list with lines
with open('input.txt', "rt", encoding="utf-8") as f:
    lines = f.readlines()

print('type date, below is example of format')
print('20210807')
date = input()

for line in lines:
    if line.count('*') == 1:
        idOfLine = lines.index(line)
        idOfDate = line.find('*') - 2
        newLine = line.replace('*', '.png">')
        newLine = newLine[:idOfDate] + '<img src="' + date + newLine[idOfDate:]
        lines.remove(line)
        lines.insert(idOfLine, newLine)

with open('output.txt', "wt", encoding="utf-8") as f:
    for line in lines:
        f.write("%s" % line)

print('job finished')
