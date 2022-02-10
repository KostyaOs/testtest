import pandas as pd

description_path = 'D:/storage/pycharmProjects/project1/digi/description.tsv'
description = pd.read_csv(
	description_path, 
	sep='\t',
	)

todo = description.copy() ##first column of desription table
done = pd.DataFrame(columns = todo.columns)## will be filled with elements from todo

command = ''
while command != 'выход':
    # update sorting
    todo.sort_values(['привязка ко времени дня','напряжение глаз', 'длительность'],ascending=[True, True, False], inplace=True)

    print('\n***К ВЫПОЛНЕНИЮ***')
    print(todo) ##

    print('\n***УЖЕ СДЕЛАНО***')
    print(done) ##
        
    command = input('\n***ОБЩЕНИЕ С ЦИФРИКОМ***\nЧтобы обновить списки, нажми Enter\nЧтобы отметить выполненное действие, введи его индекс и нажми Enter\nЧтобы выключить цифрик, введи "выход" и нажми Enter\n')
    if command.isdigit():
        while command.isdigit():
            print('это число')
            id = int(command)
            #print(todo.loc[id])
            #exit()##
            done = done.append(todo.loc[id], ignore_index=True)
            todo.drop(id, inplace=True)
            command = input()

# eye-easy first
# long first
# timelocked are last until their time comes
    