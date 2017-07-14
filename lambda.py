import boto3
import json
import random
from time import sleep
import time
from datetime import datetime

client = boto3.client('iot-data', region_name='$REGION')

def lambda_handler(event, context):

    response = client.publish(
        topic='$TOPIC',
        qos=1,
        payload=json.dumps({"temperature":str(random.randrange(60, 80)) , "pressure-1":str(random.randrange(40, 60)) , "pressure-2":str(random.randrange(40, 50)) , "vibration":str(random.randrange(50, 100)) , "timestamp":int(time.time()) })
    )

    return response