print('type how many words there are')
number = int(input())
print('type column of words')
for i in range(number):
    word = input()
    if len(word) < 4:
        print(word)
    else:
        print(word[:4])

print('job finished')
