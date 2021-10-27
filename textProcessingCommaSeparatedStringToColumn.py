print('type string')
string = input()
result = list(string.split(','))
for i in result:
    if i != '':
        print(i)

print('job finished')
