from datetime import datetime, date, time


date0 = date(2021, 10, 24)
date1 = datetime.date(datetime.now())
delta = date1 - date0
print(delta.days)

