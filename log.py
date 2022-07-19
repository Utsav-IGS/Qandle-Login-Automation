import csv
import os
from datetime import datetime, timedelta

from  setup import Setup

class Log(Setup):
    
    def __init__(self, clock_in_time=None):
        Setup.__init__(self)
        self.weekDays = ("Monday", "Tuesday", "Wednesday",
                         "Thursday", "Friday", "Saturday", "Sunday")
        self.today_date =  datetime.today().date()
        self.today_day = self.weekDays[datetime.today().weekday()]
        self.clock_in_time = clock_in_time
        self.clock_out_time = timedelta(hours=self.get_user_credentials(
            "total_work_hours").hour) + timedelta(hours=self.clock_in_time.hour, minutes=self.clock_in_time.minute, seconds=self.clock_in_time.second) if self.clock_in_time else None
        self.data = {
            "date": self.today_date,
            "weekday": self.today_day,
            "clock_in_time": self.clock_in_time,
            "clock_out_time": self.clock_out_time,
        }
        if self.log_file_exists and self.clock_in_time and self.clock_out_time and self.clocked_in_today:
            self.write_csv(data=self.data)
            
        
    def write_csv(self, data: dict):
        if self.log_file_exists:
            with open("config_files/daily_log.csv", "a+") as log_file:
                fieldnames = [key for key in data]
                writer = csv.DictWriter(log_file, fieldnames=fieldnames, lineterminator="\n")
                if os.stat("config_files/daily_log.csv").st_size == 0:
                    writer.writeheader()
                writer.writerow(data)
    
    def read_csv(self):
        all_data = {}
        with open("config_files/daily_log.csv") as log_file:
            reader = csv.DictReader(log_file)
            for row in reader:
                all_data[row.get('date')] = row
        return all_data       
    
    def clocked_in_today(self) -> bool:
        return True if self.read_csv().get(str(self.today_date)) is not None else False
    
    def log_file_exists(self) -> bool:
        try:
            with open('config_files/daily_log.csv', 'r') as file:
                return True
        except Exception:
            open('config_files/daily_log.csv', 'w+')
            return True
        
if __name__ == "__main__":
    time = datetime.strptime("09:00:00", "%H:%M:%S").time()
    print(time)
    log = Log(time)
    print(log.read_csv().get(str(log.today_date)))
    print(log.clocked_in_today())
