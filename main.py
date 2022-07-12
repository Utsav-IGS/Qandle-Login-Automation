from qandle import Qandle
from time import sleep

from setup import Setup

creds = Setup()
qandle = Qandle()
qandle.login(email=creds.get_user_credentials("email"), password=creds.get_user_credentials("password"))

sleep(5)
qandle.clock_in()

# qandle.clock_out()