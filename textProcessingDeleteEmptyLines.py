mylist = []
signal = 'none'
while signal != '0':
    signal = input()
    if signal != '':
        mylist.append(signal)

for i in mylist:
    print(i)


print('job finished')
