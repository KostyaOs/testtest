import pandas as pd
import os
import datetime


    
# check if program ran today

# Turn current day to string
now = datetime.datetime.now()
today = now.strftime("%d")

# read current day from file
today_path = 'D:/storage/pycharmProjects/project1/digi/date.txt'
logday = open(today_path, 'r', encoding='utf-8').read()
logday = logday[:2]
print(logday)

# load paths
todo_path = 'D:/storage/pycharmProjects/project1/digi/todo.tsv'
done_path  = 'D:/storage/pycharmProjects/project1/digi/done.tsv'

# if there are no record from today
if today != logday:
    
    # load from blanks  
    description_path = 'D:/storage/pycharmProjects/project1/digi/description.tsv'
    description = pd.read_csv(
        description_path, 
        sep='\t',
        )
    
    todo = description.copy() 
    done = pd.DataFrame(columns = todo.columns) # empty dataframe with same column names as todo

    # save todo table as file (so that notifier could pick up on it)
    todo.to_csv(
        todo_path, 
        sep='\t', 
        index = False # says do NOT write index column to table file
        )
else:
    
    # load from logs
    
    todo = pd.read_csv(
        todo_path, 
        sep='\t',
        )
    done = pd.read_csv(
        done_path, 
        sep='\t',
        )


command = ''
while command != 'выход':
    os.system('cls') # clear console 
    command = input('\n* ГЛАВНОЕ МЕНЮ *\nопции:\nминимум\nповторения\nвыход\n')    
    if command == 'минимум':
        # code for minimum page    
        expected = ['перезагрузить','выполнил', 'главное меню','выход', 'сунгадоро']
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
                    
                    comment = '\nопции:\nперезагрузить\nвыполнил\nсунгадоро\nглавное меню\nвыход\n'
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
                    
                    # save todo and done table as files
                    todo.to_csv(
                        todo_path, 
                        sep='\t', 
                        index = False # says do NOT write index column to table file
                        )
                    done.to_csv(
                        done_path, 
                        sep='\t', 
                        index = False # says do NOT write index column to table file
                        )
                    
                    # write current day to logs (when tables get updated)
                    open(today_path, 'w', encoding='utf-8').write(today)

                    comment = 'могу принять новую команду\n'
                                        
                if command == 'сунгадоро':
                    
                    # ask for  eyestrain effect 
                    # ask for  work duration 
                    # try selecting by eyestrain effect
                    # try selecting by duration
                    # try selecting by daytime dependency
                    # sort so that highest duration will be on top
                    
                    spare_eyes = input('Do you need eyes to rest during this break? (yes / no)\n')
                    while  spare_eyes not in ['yes', 'no']:
                         spare_eyes = input('Wrong format. Try again\n')

                    work_duration = input('How many minutes did you work?\n')
                    while not work_duration.isdigit():
                        work_duration = input('Wrong format. Try again\n')
                    work_duration = int(work_duration)
                    
                    #min_break = work_duration // 4##
                    max_break = work_duration // 3
                        
                    now = datetime.datetime.now()
                    evening_start = now.replace(hour=17, minute=0, second=0, microsecond=0)
                    
                    if now < evening_start:
                        time_dependent = False
                    else:
                        time_dependent = True
                        
                    if  spare_eyes == 'yes':
                        strain = False
                    else:
                        strain =   True

                    possible_rows = todo.copy()
                    filter = 1
                    while len(possible_rows.index) != 0:
                        selected_rows = possible_rows.copy()
                        if filter == 1:
                            possible_rows = possible_rows[possible_rows['напряжение глаз'] == strain]
                            print(possible_rows)
                        elif filter == 2:
                            print('got to 2')
                            #possible_rows = possible_rows[possible_rows['длительность'] >= min_break]##
                            possible_rows = possible_rows[possible_rows['длительность'] <= max_break]
                            print(possible_rows)
                        elif filter == 3:
                            print('got to 3')
                            possible_rows = possible_rows[possible_rows['привязка ко времени дня'] == time_dependent]
                            print(possible_rows)

                        elif filter == 4:
                            print('got to 4')
                            print(possible_rows)
                            break
                        filter += 1
                    selected_rows.sort_values(['длительность'],ascending=False,inplace=True)
                    selected_rows = selected_rows.reset_index(drop=True)
                    print('Here are most fit tasks:')
                    print(selected_rows)
                
            else:	# if command is nonsense
                comment = 'для такого ввода нет команды, давай еще раз\n'

            command = input(comment)
            if command == 'выход':
                exit()
    elif command == 'повторения':
    
        # code for revisions page
        
        print('\nраздел еще не написал этот')




# eye-easy first
# long first
# timelocked are last until their time comes