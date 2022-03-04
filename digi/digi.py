import pandas as pd
import os
import datetime
from playsound import playsound


    
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
while command != 'exit':
    os.system('cls') # clear console 
    command = input('\n* MAIN MENU *\noptions:\nminimum\nuni check\nexit\n')    
    if command == 'minimum':
        # code for minimum page    
        expected = ['reload','completed', 'main menu','exit', 'sungadoro']
        command = 'reload' # so that program shows activities first 
        while command != 'main menu':
            if command in expected: # if command makes sense
                if command == 'reload':
                    os.system('cls') # clear console 

                    # resort
                    # show todo
                    # show done
                    
                    todo.sort_values(['for evening','eye strain', 'duration'],ascending=[True, True, False], inplace=True)

                    print('\n* TODO *')
                    print(todo) ##

                    print('\n* DONE *')
                    print(done) ##
                    
                    comment = '\noptions:\nreload\ncompleted\nsungadoro\nmain menu\nexit\n'
                if command == 'completed':
                    # ask to type indexes of completed activities and check check that all indexes make sense
                    comment = 'type indexes of completed tasks\n'
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

                    comment = 'ready to get next command\n'
                                        
                if command == 'sungadoro':
                    
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
                            possible_rows = possible_rows[possible_rows['eye strain'] == strain]
                            print(possible_rows)
                        elif filter == 2:
                            print('got to 2')
                            #possible_rows = possible_rows[possible_rows['duration'] >= min_break]##
                            possible_rows = possible_rows[possible_rows['duration'] <= max_break]
                            print(possible_rows)
                        elif filter == 3:
                            print('got to 3')
                            possible_rows = possible_rows[possible_rows['for evening'] == time_dependent]
                            print(possible_rows)

                        elif filter == 4:
                            print('got to 4')
                            print(possible_rows)
                            break
                        filter += 1
                    selected_rows.sort_values(['duration'],ascending=False,inplace=True)
                    selected_rows = selected_rows.reset_index(drop=True)
                    print('Here are most fit tasks:')
                    print(selected_rows)
                    
                    # start timer
                        # print('Type 'cancel' to cancel timer')
                    # We learn what time it is now, learn how many minutes we should add, then find what time to stop timer. Then we plug hours and minutes of that time into separate variables for time checking part of code 
                    # now = time.now()
                    # duration = input()
                    # future = now + duration

                    now = datetime.datetime.now()
                    duration = max_break
                    half_duration = datetime.timedelta(hours=0, minutes = duration // 2,seconds=0)
                    duration = datetime.timedelta(hours=0, minutes = duration,seconds=0)
                    future = now + duration
                    half_future = now + half_duration

                    alarmH = future.hour
                    alarmM = future.minute
                    alarmS = future.second
                    
                    halfH = half_future.hour
                    halfM = half_future.minute
                    halfS = half_future.second               
                  
                    print("half alarm at",halfH,halfM,halfS)
                    print("full alarm at",alarmH,alarmM,alarmS)

                    beyond_half_over = False
                    while(1 == 1):
                        
                        over = (alarmH == datetime.datetime.now().hour and
                                alarmM == datetime.datetime.now().minute and alarmS <= datetime.datetime.now().second)
                        half_over = (halfH == datetime.datetime.now().hour and
                                halfM == datetime.datetime.now().minute and halfS <= datetime.datetime.now().second)
                        if over :
                            print("Break is over")
                            playsound('D:/storage/pycharmProjects/project1/digi/beep-01a.mp3')
                            break
                        if half_over and not beyond_half_over:
                            print("Half of break is over")
                            playsound('D:/storage/pycharmProjects/project1/digi/beep-01a.mp3')
                            beyond_half_over = True
                
                    comment = 'ready to get next command\n'

                if command == 'exit':
                    exit()
            else:	# if command is nonsense
                comment = 'Wrong format. Try again\n'

            command = input(comment)

    elif command == 'uni check':
        
        expected = ['main menu','exit', 'reload']
        command = 'reload'
        while command != 'main menu':
            if command in expected: # if command makes sense
                if command == 'reload':
                    os.system('cls') # clear console 

                    # get inputs
                    # form plan
                    
                    water = input('Do you need to take water? (yes / no)\n')
                    food = input('Do you need to take food? (yes / no)\n')
                    money = input('Do you need a lot of money? (Bus, food expenses) (yes / no)\n')
                    
                    plan = 'Here is plan for item fetching:\n\n'
                    
                    plan += 'Go wash your hands. After that, in following order, take things that need clean hands\n'
                    if water == 'yes' or food == 'yes':
                        plan += '(kitchen)\n'
                    if water =='yes':
                        plan += 'water\n'
                    if food=='yes':
                        plan += 'food\n'
                    plan += '(dresser)\n'
                    plan += 'mask\n\n'

                    plan += 'For following items there is no need for clean hands. Follow order to reduce time for fetching\n'
               
                    plan += '(dresser)\n'
                    plan += 'socks\n'
                    plan += 'spare cloth\n'

                    plan += '(desk)\n'
                    plan += 'earbuds\n'
                    plan += 'paper and pen\n'
                    plan += 'phone\n'
                    
                    plan += '(backpack)\n'
                    plan += 'documents\n'
                    plan += 'sleepers\n'
                    
                    plan += '(entrance)\n'    
                    if money =='yes':
                        plan += 'A LOT OF '
                    plan += 'money\n'
                    plan += 'keys\n'

                    print(plan)

                    comment = '\noptions:\nreload\nmain menu\nexit\n'
                    
                if command == 'exit':
                    exit()
            else:	# if command is nonsense
                comment = 'Wrong format. Try again\n'

            command = input(comment)

           


# eye-easy first
# long first
# timelocked are last until their time comes