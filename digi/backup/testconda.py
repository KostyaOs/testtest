import pandas as pd

print(pd.__version__)

description_path = 'D:/storage/pycharmProjects/project1/digi/description.tsv'
df = pd.read_csv(
	description_path, 
	sep='\t',
	)
print(df)


print('Hello world!')
i = ''
while i == '':
    i = input('waiting for your input')
    