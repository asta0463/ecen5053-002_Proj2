# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 14:50:43 2017

@author: Aakash
"""
import threading
from tinydb import TinyDB, Query
from datetime import datetime
import sensorRead as sensorRead

dbSamplingInterval=5 # interval in seconds when data is updated in the database

db = TinyDB('proj2Db.json')

def addDataToDb(): 
    """ function to update temp, humidity into database """
    global dbSamplingInterval
    
    threading.Timer(dbSamplingInterval,addDataToDb).start() # to autorun function once every update interval
    
    humidity, temperature = sensorRead.get_TempHum() #read temperature and humidity
    db.insert({'timestamp_year': datetime.now().year,'timestamp_month': datetime.now().month,
               'timestamp_day': datetime.now().day,'timestamp_hour': datetime.now().hour,
               'timestamp_minute': datetime.now().minute,'timestamp_second': datetime.now().second,
               'temperature':temperature,'humidity':humidity})

def maketimestamp(item):
    
    return datetime(item['timestamp_year'],item['timestamp_month'],item['timestamp_day'],
        item['timestamp_hour'],item['timestamp_minute'],item['timestamp_second'])    
    
def showdb():
    """ function to display all items in database in timestamp, temp , humidity format,
    to be used for debugging purposes"""
    print("date"," ","time"," ","temperature"," ","humidity")
    for item in db:
        print(datetime(item['timestamp_year'],item['timestamp_month'],item['timestamp_day'],
        item['timestamp_hour'],item['timestamp_minute'],item['timestamp_second'])
        ,"", item['temperature'],item['humidity'])


    
    
def calcAverage(key):
    """ function to calculate average of temperature of humidity or temperature
    the required can be passed as a string to the function """
    total=0
    ts=Query()
    res=db.search((ts.timestamp_minute==20) & (ts.timestamp_second>10))
    for i in res:
        total=total+i[key]
    return total/len(res)    

print(calcAverage("temperature"))    
#def getaverage():
    
#dt2day=datetime.today()

 