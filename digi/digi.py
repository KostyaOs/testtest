import pandas as pd
import os


description_path = 'D:/storage/pycharmProjects/project1/digi/description.tsv'
description = pd.read_csv(
	description_path, 
	sep='\t',
	)

todo_path = 'D:/storage/pycharmProjects/project1/digi/todo.tsv'
todo = description.copy() ##first column of desription table

# save todo table as file
todo.to_csv(
    todo_path, 
    sep='\t', 
    index = False # says do NOT write index column to table file
    )

done = pd.DataFrame(columns = todo.columns)## will be filled with elements from todo

command = ''
while command != 'выход':
    os.system('cls') # clear console 
    command = input('\n* ГЛАВНОЕ МЕНЮ *\nопции:\nминимум\nповторения\nвыход\n')    
    if command == 'минимум':
        # code for minimum page    
        expected = ['перезагрузить','выполнил', 'главное меню','выход']
        command = 'перезагрузить' # so that program shows activities first 
        while command != 'главное меню':
            if command in expected: # if command makes sense
                if command == 'перезагрузить':
                    os.system('cls') # clear console 

                    # resort
                    # show todo
                    # show done
                    
                    todo.sort_values(['привязка ко времени дня','напряжение глаз', 'длительность'],ascending=[True, True, False], inplace=True)

                    print('\n***К ВЫПОЛНЕНИЮ***')
                    print(todo) ##

                    print('\n***УЖЕ СДЕЛАНО***')
                    print(done) ##
                    
                    comment = '\nопции:\nперезагрузить\nвыполнил\nглавное меню\nвыход\n'
                if command == 'выполнил':
                    # ask to type indexes of completed activities and check check that all indexes make sense
                    comment = 'введи индексы выполненных задач\n'
                    nonsense = True # True if input is nonsense
                    while nonsense:	# while input makes no sense			
                        try:
                            indexes = list(map(int, input(comment).split(' '))) # check that all inputs are integers
                            nonsense = False

                            # check that all numbers are present in todo indexes list
                            possible_ids = list(todo.index.values)
                            for id in indexes:
                                if id not in possible_ids: ##
                                    nonsense = True
                            
                        except ValueError: ## find out what type of error it actualy is
                            nonsense = True
                                     
                    # for each index in indexes
                        # move it from todo to done                                     
                    for id in indexes:
                        done = done.append(todo.loc[id], ignore_index=True)
                        todo.drop(id, inplace=True)
                        command = input()
                    
                    comment = 'могу принять новую команду\n'
            else:	# if command is nonsense
                comment = 'для такого ввода нет команды, давай еще раз\n'
            
            # save todo table as file
            todo.to_csv(
                todo_path, 
                sep='\t', 
                index = False # says do NOT write index column to table file
                )

            
            command = input(comment)
            if command == 'выход':
                exit()
    elif command == 'повторения':
    
        # code for revisions page
        
        print('\nраздел еще не написал этот')




# eye-easy first
# long first
# timelocked are last until their time comes