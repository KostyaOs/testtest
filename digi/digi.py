import pandas as pd
import os


description_path = 'D:/storage/pycharmProjects/project1/digi/description.tsv'
description = pd.read_csv(
	description_path, 
	sep='\t',
	)

todo = description.copy() ##first column of desription table
done = pd.DataFrame(columns = todo.columns)## will be filled with elements from todo

command = ''
while command != 'выход':
    os.system('cls') # clear console 
    command = input('\n* ГЛАВНОЕ МЕНЮ *\nопции:\nминимум\nповторения\nвыход\n')    
    if command == 'минимум':
        # code for minimum page    

        reloads = ['минимум', '']
        breaks = ['выход', 'главное меню']
        while command not in breaks:

            if command not in reloads:
                comment = 'для такого ввода нет опции, попробуй еще раз\n'
                command = input(comment)
            else:
                # update sorting
                todo.sort_values(['привязка ко времени дня','напряжение глаз', 'длительность'],ascending=[True, True, False], inplace=True)

                print('\n***К ВЫПОЛНЕНИЮ***')
                print(todo) ##

                print('\n***УЖЕ СДЕЛАНО***')
                print(done) ##
                    
                command = input('\nопции:\n[Enter] (обновить списки)\n<индекс> (отметить выполненное действие)\nглавное меню\nвыход\n')
                
                # если ввел индекс
                ids = list(todo.index.values)
                while command.isdigit() and (int(command) in ids):
                    id = int(command)
                    print('отметил выполнение минимума -', todo.loc[id]['название'])
                    done = done.append(todo.loc[id], ignore_index=True)
                    todo.drop(id, inplace=True)
                    command = input()
                    
                    
        # show todo and done
        # while command is not in break commands list 
            # tell what commands are available
            # ask for command
            # if command makes sense
                # execute
            # else:
                # say it is nonsense
                #return to #ask for command
    elif command == 'повторения':
    
        # code for revisions page
        
        print('\nраздел еще не написал этот')




# eye-easy first
# long first
# timelocked are last until their time comes