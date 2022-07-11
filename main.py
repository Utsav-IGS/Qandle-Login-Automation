from qandle import Qandle
from time import sleep

qandle = Qandle()
qandle.login(email="", password="")

sleep(5)
if qandle.get_logged_hours() == qandle.convert_time("00:00:00"):
    qandle.clock_in()
else:    
    sleep(5)
    qandle.clock_out()