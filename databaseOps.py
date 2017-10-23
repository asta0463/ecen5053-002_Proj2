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

def getData(unit):
    """ function to get latest data from sensors , 
    accounts for unit change from the webpage and
    converts temperature values accordingly"""
    h,t= sensorRead.get_TempHum()
    if(t==None):
        t=-1
    if(h==None):
        h=-1
    if(unit==1):
        t=sensorRead.todegF(t)
    return (str(round(t,2))+','+str(round(h,2)))

def ws_cur_data(unit):
    """function to provide temp and humidity data in the format that the jquery script needs
    All data to websocket gets sent in a combined packet formatted as
    requested_data_name,timestamp,temp,[humidity] 
    the last parameter can be 1 or 2 depending on requested data
    all of the data is formatted as string and then sent out"""
    return('cur_data'+','+datetime.now().strftime('%b-%d-%Y %H:%M:%S')+','+getData(unit))

def ws_avg_temp(unit):
    """function to provide average temp data in the format that the jquery script needs"""
    ts,val = calcDayAverage("temperature")
    if(unit==1):
        val=sensorRead.todegF(val)
    return('avg_temp'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_max_temp(unit):
    """function to provide maximum temp data in the format that the jquery script needs"""
    ts,val = calcDayMaximum("temperature")
    if(unit==1):
        val=sensorRead.todegF(val)
    return('max_temp'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_min_temp(unit):
     """function to provide minimum temp data in the format that the jquery script needs"""
     ts,val = calcDayMinimum("temperature")
     if(unit==1):
        val=sensorRead.todegF(val)
     return('min_temp'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))        
    

def ws_last_temp(unit):
    """function to provide last value of temp from database 
    in the format that the jquery script needs"""
    ts,val = calcLastVal("temperature")
    if(unit==1):
        val=sensorRead.todegF(val)
    return('last_temp'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_last_hum():
    """function to provide last value of humidity from database 
    in the format that the jquery script needs"""
    ts,val = calcLastVal("humidity")
    return('last_hum'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_avg_hum():
    """function to provide average humidity data 
    in the format that the jquery script needs"""
    ts,val = calcDayAverage("humidity")
    return('avg_hum'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_max_hum():
    """function to provide maximum humidity data 
    in the format that the jquery script needs"""
    ts,val = calcDayMaximum("humidity")
    return('max_hum'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def ws_min_hum():
    """function to provide minimum humidity data 
    in the format that the jquery script needs"""
    ts,val = calcDayMinimum("humidity")
    return('min_hum'+','+ts.strftime('%b-%d-%Y %H:%M:%S')+','+str(round(val,2)))

def addDataToDb(): 
    """ function to update temp, humidity into database 
    the timestamp is split into different keys for year,month , day, hour, min and sec 
    as tinydb cannot read in the python datetime type"""
    global dbSamplingInterval,docId
    
    threading.Timer(dbSamplingInterval,addDataToDb).start() # to autorun function once every update interval
    
    humidity, temperature = sensorRead.get_TempHum() #read temperature and humidity
    if(temperature==None):
        temperature=-1
    if(humidity==None):
        humidity=-1
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

def calcLastVal(key):
    """ function to get last value of temperature or humidity for current day,
    the required param temperature/humidity can be passed as a string to the function """
    lastRec=db.all()[0]
    return getDateTime(lastRec),lastRec[key]

def calcDayMinimum(key):
    """ function to calculate minimum of temperature or humidity for current day,
    the required param temperature/humidity can be passed as a string to the function """
    curTime=datetime.now()
    ts=Query()
    res=db.search((ts.timestamp_year==curTime.year) & (ts.timestamp_month==curTime.month) &
    (ts.timestamp_day== curTime.day))
    minRec=min(res, key=lambda x:x[key])
    return getDateTime(minRec),minRec[key]

    
 