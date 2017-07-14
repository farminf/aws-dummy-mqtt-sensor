#!/usr/bin/env python
# imports
import sys
import os
import ConfigParser
import threading
import multiprocessing
from time import sleep
import time
from datetime import datetime
import json
# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import AWSIoTPythonSDK
sys.path.insert(0, os.path.abspath(AWSIoTPythonSDK.__file__))
# You can start importing the exceptions now
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishError
import ast



class sendData:




    
    #Read From Config.ini
    config = ConfigParser.ConfigParser()
    config.read('./config.ini')
    config.sections()
    device_id = ast.literal_eval(config.get('general', 'device_id'))

    
    myMQTTClient = AWSIoTMQTTClient(device_id)
    myMQTTClient.configureEndpoint(ast.literal_eval(config.get('amazon', 'url')), config.getint('amazon', 'port'))
    myMQTTClient.configureCredentials(ast.literal_eval(config.get('amazon', 'aws_root')), ast.literal_eval(config.get('amazon', 'pri_key'))
                                        , ast.literal_eval(config.get('amazon', 'pri_cert')))
    # Con Conf
    myMQTTClient.configureAutoReconnectBackoffTime(1, 2, 20)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    topic = ast.literal_eval(config.get('amazon', 'topic'))


    def __init__(self):
        print("class initiated")
        self.aws_thread_success = False
        self.is_mqtt_connect = False
        try:
            self.myMQTTClient.connect()
        except:
            print("AWS MQTT not connected ")
        else:
            self.is_mqtt_connect = True

    # Function for sending a message to AWS IoT
    def send_to_aws(self,payload):
        print("send  to AWS")
        self.aws_thread_success = False
        if self.is_mqtt_connect == True:
            timestamp =  int(time.time())
            result_json = payload
            try:
                self.myMQTTClient.publish(self.topic , json.dumps(result_json) , 0)
            except publishQueueDisabledException as e:
                print("Offline publish queue is disabled!")
                return self.aws_thread_success
            except publishQueueFullException as e:
                print("Offline publish queue is full!")
                return self.aws_thread_success
            except e:
                print (e)
                return self.aws_thread_success
            else:
                print("msg sent to AWS")
                self.aws_thread_success = True
        else:
            self.aws_thread_success = False


    def run(self, payload):
        
        aws_thread = threading.Thread(target=self.send_to_aws(payload), args=(self.aws_thread_success,)).start()
        print("aws: " +str(self.aws_thread_success))
        if self.aws_thread_success == True:
            return True
        else:
            return False
