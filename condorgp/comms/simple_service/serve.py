#!/usr/bin/python

import os
# from condorgp.comms.simple_message import send
# condorgp/comms/simple_message/send.py
from condorgp.comms.simple_message import send
print("SERVICE STARTED")

while True:
    # time.sleep(1)
    value = int(input("Enter command: "))

    print(f'You entered {value}')

    if value == 88:
        exit()
    elif value == 1:
        send.send()
