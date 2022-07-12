import os
from encrpyt import Encrypt
from time import strftime, strptime
from datetime import datetime, timedelta, time
import json

class Setup(Encrypt):
    def __init__(self):
        Encrypt.__init__(self)
        self.user_email = ""
        self.user_password = ""
        self.preffered_clockin_time = ""
        self.preffered_clockout_time = ""
        self.total_work_hours = ""
        if not self.config_exists():
            print("-"*100)
            print("- The following prompt will ask your qandle email, password, preffered clock in and\n  clock out time.")
            print("- The email and password are encrypted and then saved in the file as encrypted strings.")
            print("- The data is saved in a file called 'config.json' at the root level of the project")
            print("-"*100+"\n")
            self._get_user_email()
            self._get_user_password()
            self._get_user_clockin_time()
            self._get_user_clockout_hours()
            self.total_work_hours = self.preffered_clockout_time - self.preffered_clockin_time
            self.write_config()
        else:
            with open("config_files/config.json") as config:
                data = json.load(config)
                self.user_email = data.get("email").encode()
                self.user_password = data.get("password").encode()
                self.preffered_clockin_time = datetime.strptime(
                    data.get("clock_in_time"), "%H:%M:%S")
                self.preffered_clockout_time = datetime.strptime(
                    data.get("clock_out_time"), "%H:%M:%S")
                self.total_work_hours = datetime.strptime(
                    data.get("total_work_hours"), "%H:%M:%S")
        
        
    def _get_user_email(self):
        self.user_email = self.encrypt(input("- Enter your Qandle Email: "))
        
    def _get_user_password(self):
        self.user_password = self.encrypt(input("- Enter your Qandle Password: "))
    
    def _get_user_clockout_hours(self):
        self.preffered_clockout_time = self.preffered_clockin_time + timedelta(hours=int(input("\n- Enter the amount of hours you need to log in Qandle:\nExample - 09\n")))
    
    def _get_user_clockin_time(self):
        print("\n- Enter the preffered Clock in time in 24 hour format:\nExample - 09:00:00, 13:00:00")
        self.preffered_clockin_time = datetime.strptime(input(), "%H:%M:%S")
    
    def config_exists(self):
        try:
            if os.path.exists("config_files/config.json") and os.stat("config_files/config.json").st_size > 0:
                return True
        except FileNotFoundError:
            return False
    
    def write_config(self):
        path = "config_files/config.json"
        
        # Data to be written
        user_data = {
            "email": self.user_email.decode(),
            "password": self.user_password.decode(),
            "clock_in_time": self.preffered_clockin_time.time().isoformat(),
            "clock_out_time": self.preffered_clockout_time.time().isoformat(),
            "total_work_hours": "0"+str(self.total_work_hours),
        }

        # Serializing json
        json_object = json.dumps(user_data, indent=4)

        # Writing to sample.json
        try:
            with open(path, "w+") as outfile:
                outfile.write(json_object)
        except Exception:
            return FileNotFoundError("File does not exists")
            
    def get_user_credentials(self, required_data):
        data = ""
        if self.config_exists():
            with open("config_files/config.json") as outfile:
                data = json.load(outfile)
                if required_data == "email" or required_data == "password":
                    return self.decrypt(data.get(required_data).encode())
                else:
                    return datetime.strptime(data.get(required_data), "%H:%M:%S").time()
    
    
if __name__ == "__main__":
    setup = Setup()
    print(setup.get_user_credentials(required_data="email"))
    print(setup.get_user_credentials(required_data="password"))
    print(setup.get_user_credentials(required_data="clock_in_time"))
    print(setup.get_user_credentials(required_data="clock_out_time"))
    print(setup.get_user_credentials(required_data="total_work_hours"))
    
    