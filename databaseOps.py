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
    """ function to update temp, humidity into database 
    the timestamp is split into different keys for year,month , day, hour, min and sec 
    as tinydb cannot read in the python datetime type"""
    global dbSamplingInterval
    
    threading.Timer(dbSamplingInterval,addDataToDb).start() # to autorun function once every update interval
    
    humidity, temperature = sensorRead.get_TempHum() #read temperature and humidity
    db.insert({'timestamp_year': datetime.now().year,'timestamp_month': datetime.now().month,
               'timestamp_day': datetime.now().day,'timestamp_hour': datetime.now().hour,
               'timestamp_minute': datetime.now().minute,'timestamp_second': datetime.now().second,
               'temperature':temperature,'humidity':humidity})

def getDateTime(ts):
    """Converts the multiple key/values from db into single time stamp of the datetime type"""
    return datetime(ts['timestamp_year'],ts['timestamp_month'],ts['timestamp_day'],
        ts['timestamp_hour'],ts['timestamp_minute'],ts['timestamp_second'])    

def getDate(ts):
    """ same as above function but to get a date without time stamp"""
    return getDateTime(ts).date()

def getTime(ts):
    """ same as above function but to get a time without date"""
    return getDateTime(ts).time()

    
def showdb():
    """ function to display all items in database in timestamp, temp , humidity format,
    to be used for debugging purposes"""
    print("date"," ","time"," ","temperature"," ","humidity")
    for item in db:
        print(getDateTime(item),",", item['temperature'],",",item['humidity'])
   
    
def calcDayAverage(key):
    """ function to calculate average of temperature or humidity for current day,
    the required param temperature/humidity can be passed as a string to the function """
    curTime=datetime.now()
    total=0
    ts=Query()
    res=db.search((ts.timestamp_year==curTime.year) & (ts.timestamp_month==curTime.month) &
    (ts.timestamp_day== curTime.day))
    for i in res:
        total=total+i[key]
    if(len(res)>0):
        avg=total/len(res)
    else:
        avg=0
    return curTime,avg  

def calcDayMaximum(key):
    """ function to calculate maximum of temperature or humidity for current day,
    the required param temperature/humidity can be passed as a string to the function """
    curTime=datetime.now()
    ts=Query()
    res=db.search((ts.timestamp_year==curTime.year) & (ts.timestamp_month==curTime.month) &
    (ts.timestamp_day== curTime.day))
    maxRec=max(res, key=lambda x:x[key])
    return getDateTime(maxRec),maxRec[key]

def calcDayMinimum(key):
    """ function to calculate minimum of temperature or humidity for current day,
    the required param temperature/humidity can be passed as a string to the function """
    curTime=datetime.now()
    ts=Query()
    res=db.search((ts.timestamp_year==curTime.year) & (ts.timestamp_month==curTime.month) &
    (ts.timestamp_day== curTime.day))
    minRec=min(res, key=lambda x:x[key])
    return getDateTime(minRec),minRec[key]

#showdb()
#print(datetime(datetime.now().year,datetime.now().month,datetime.now().day).time())
#print(calcAverage("temperature"))    
t,v=calcDayMaximum("temperature")
print(t.strftime('%b-%d-%Y %H:%M:%S')," ",v)
    
 