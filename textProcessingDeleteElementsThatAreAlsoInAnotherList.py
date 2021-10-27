print('how many questions are in test?')
total = int(input())

result = []
for i in range(1, total + 1):
    result.append(i)

print('how many elements to be deleted?')
amountToDelete = int(input())

print('paste column of elements to be removed')
for i in range(amountToDelete):
    result.remove(int(input()))

print('here is the result')
for i in result:
    print(i)
