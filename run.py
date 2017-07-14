#!/usr/bin/env python
# Library imports
from time import sleep
import time
from datetime import datetime
import json
from send_data import sendData
import random



send_data = sendData()
# check if MQTT client is connected to Broker
if send_data.is_mqtt_connect == False:
    print ("MQTT client is not Connected")


while True:
    payload = {"temperature":str(random.randrange(60, 80)) , "pressure-1":str(random.randrange(40, 60)) , "pressure-2":str(random.randrange(40, 50)) , "vibration":str(random.randrange(50, 100)) , "timestamp":int(time.time())}
    send_data.run(payload)
    time.sleep(10)