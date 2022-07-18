from log import Log
from qandle import Qandle
from time import sleep
from setup import Setup

from datetime import datetime, timedelta

log = Log()

def is_weekend() -> bool:
    return datetime.today().weekday() >= 5

if not is_weekend() and not log.clocked_in_today():
    user_input = input("Would you like to clock in today? (Y or N) [Default = Y]: ")
    if user_input.upper() == "Y":
        qandle = Qandle()
        creds = Setup()
        qandle.login(email=creds.get_user_credentials("email"), password=creds.get_user_credentials("password"))
        sleep(5)
        qandle.clock_in()
else:
    print("Clocked in Data Exists...")

current_time = datetime.now().time()
clock_out_time = datetime.strptime(log.read_csv().get(str(log.today_date)).get('clock_out_time'), "%H:%M:%S").time()

is_time_remaining = timedelta(hours=clock_out_time.hour,
                           minutes=clock_out_time.minute, seconds=clock_out_time.second) > timedelta(hours=current_time.hour,
          minutes=current_time.minute, seconds=current_time.second)
difference = timedelta(hours=clock_out_time.hour, minutes=clock_out_time.minute, seconds=clock_out_time.second) - timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) if is_time_remaining else 0
                           
# print(clock_out_time, current_time, time_remaining)
if log.clocked_in_today and not is_time_remaining and difference == 0:
    qandle = Qandle()
    creds = Setup()
    qandle.login(email=creds.get_user_credentials("email"),
                 password=creds.get_user_credentials("password"))
    sleep(5)
    qandle.clock_out()
else:
    print(f'There is still {difference} hours remaining')