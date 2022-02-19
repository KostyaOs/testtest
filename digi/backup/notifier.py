import datetime
from win10toast import ToastNotifier
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
import os


# define function that will be called every so often by main script
def awakened():

    #load minimum_todo table
    minimum_todo = pd.read_csv(
    minimum_todo_path,
    sep='\t',
    )

    # define column name here because it is so long
    column_name = 'привязка ко времени дня'

    #check what time is it now
    now = datetime.datetime.now()

    #if it is less than evening start (if it is before evening)
    if now < evening_start:

        #if there are rows tagged with day_tag:
        if False in minimum_todo[column_name]:

            #select these rows
            selected_rows = minimum_todo[minimum_todo[column_name] == False]

            #turn name column to list
            names = selected_rows['название'].tolist()

            # write text of notification
            text = 'До вечера нужно выполнить следующие задачи:\n\n'
            for name in names:
                text += name + '\n'

    # (if it is evening)
    else:

        #if there are rows tagged with evening_tag:
        if True in minimum_todo[column_name]:

            #select these rows
            selected_rows = minimum_todo[minimum_todo[column_name] == True]

            #turn name column to list
            names = selected_rows['название'].tolist()

            # write title and text of notification
            text = 'До сна нужно выполнить следующие задачи:\n\n'
            for name in names:
                text += name + '\n'


    # write title and text of notification
    text += '\nКак насчет сходить сделать тройку-другую подтягиваний?'

    # send notification
    open(notification_filepath, 'w', encoding='utf-8').write(text)
    os.system("start " + notification_filepath)
    
    # allow to terminate program between scheduled time
    command = input("type 'exit' to terminate program\n")
    if command == 'exit':##
        os._exit(0)
    
    
    
    
    

    

# set paths
minimum_todo_path = 'D:/storage/pycharmProjects/project1/digi/todo.tsv' # this table is actually created and edited only by another script and this table is day specific
notification_filepath = 'D:/storage/pycharmProjects/project1/digi/notification.txt'


# define evening start
evening_start = datetime.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

# make job running all day
scheduler = BlockingScheduler()
hours_between = 5
scheduler.add_job(awakened, 'interval', seconds=hours_between)
scheduler.start()



