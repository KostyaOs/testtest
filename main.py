

inpt = input()
lst = []
while inpt != 'stop':
    lst.append(inpt)
    inpt = input()
result = ''
for i in lst:
    result += i + ' '
print(result)

