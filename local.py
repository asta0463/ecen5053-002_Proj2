# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 09:13:09 2017

@author: Aakash
"""
import sys
import threading
from PyQt5.QtWidgets import QApplication, QDialog
from datetime import datetime
from window_template import Ui_MainWindow
import sendgrid
from sendgrid.helpers.mail import *
import sensorRead as sensorRead
import databaseOps as dbops


#initializing all global variables
update_interval=1 # interval in mins at which data is auto updated
unit=0 # 1 is degF and 0 is degC
temp_alarm_lim=35
Phone_Num=2003004000
email=""
temperature=22
messageSent=0
#dictionary of phone companies and email/text interface
phoneCompanies={"AT&T":"@txt.att.net","T Mobile":"@tmomail.net",
                    "Sprint":"@messaging.sprintpcs.com","Virgin Mobile":"@vmobl.com",
                    "US Cellular":"@mms.uscc.net","Verizon":"@vtext.com",
                    "C U email":"@colorado.edu"}

#setting up UI
app = QApplication(sys.argv)
window = QDialog()
ui = Ui_MainWindow()
ui.setupUi(window)

sg = sendgrid.SendGridAPIClient(apikey='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') #Setting up sendgrid API key for alerts


for phCo in phoneCompanies: #adding all phone companies into the Qcombobox
    ui.phCoIn.addItem(phCo)

window.show()

def change_to_degF():
    """function to change units displayed from degC to degF"""
    global unit
    unit =1
    update_data()

def change_to_degC():
    """function to change units displayed from degF to degC"""
    global unit
    unit =0
    update_data()
    

def update_data(): 
    """ function to update temp, humidity and Alarm data on display """
    global update_interval,temperature,unit
    
    threading.Timer(60*update_interval,update_data).start() # to autorun function once every update interval
    
    humidity, temperature = sensorRead.get_TempHum()
    time=datetime.now().strftime('%b-%d-%Y %H:%M:%S')
    ui.label_updateTime.setText(time)
    
    if(unit==1 and temperature!=None): # if unit is set to degF convert temperature to degF
        temperature=sensorRead.todegF(temperature) 
    
    if(temperature==None): # handling data not being sent
        ui.lcd_temperature.display("Err")
    else:
        ui.lcd_temperature.display(temperature)
   
    if(humidity==None): # handling data not being sent
        ui.lcd_humidity.display("Err")
    else:
        ui.lcd_humidity.display(humidity)
    
    alarm_check()
    update_last_temp()
    update_avg_temp()
    update_max_temp()
    update_min_temp()
    update_last_hum()
    update_avg_hum()
    update_max_hum()
    update_min_hum()
    

def update_avg_temp():
    global unit
    ts,val = dbops.calcDayAverage("temperature")
    ui.temp_unit_2.setText('degC')
    if(unit==1):
        val=sensorRead.todegF(val)
        ui.temp_unit_2.setText('degF')
    ui.avg_temp.setText(str(round(val,2)))
    ui.avg_temp_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))

def update_last_temp():
    global unit
    ts,val = dbops.calcLastVal("temperature")
    ui.temp_unit_1.setText('degC')
    if(unit==1):
        val=sensorRead.todegF(val)
        ui.temp_unit_1.setText('degF')
    ui.last_temp.setText(str(round(val,2)))
    ui.last_temp_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))

def update_max_temp():
    global unit
    ts,val = dbops.calcDayMaximum("temperature")
    ui.temp_unit_3.setText('degC')
    if(unit==1):
        val=sensorRead.todegF(val)
        ui.temp_unit_3.setText('degF')
    ui.max_temp.setText(str(round(val,2)))
    ui.max_temp_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))    
    
def update_min_temp():
    global unit
    ts,val = dbops.calcDayMinimum("temperature")
    ui.temp_unit_4.setText('degC')
    if(unit==1):
        val=sensorRead.todegF(val)
        ui.temp_unit_4.setText('degF')
    ui.min_temp.setText(str(round(val,2)))
    ui.min_temp_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))     
    
def update_min_hum():
    ts,val = dbops.calcDayMinimum("humidity")
    ui.min_hum.setText(str(round(val,2)))
    ui.min_hum_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))        

def update_max_hum():
    ts,val = dbops.calcDayMaximum("humidity")
    ui.max_hum.setText(str(round(val,2)))
    ui.max_hum_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))    
    
def update_avg_hum():
    ts,val = dbops.calcDayAverage("humidity")
    ui.avg_hum.setText(str(round(val,2)))
    ui.avg_hum_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))    
    
def update_last_hum():
    ts,val = dbops.calcLastVal("humidity")
    ui.last_hum.setText(str(round(val,2)))
    ui.last_hum_ts.setText(ts.strftime('%b-%d-%Y %H:%M:%S'))       
    
def update_Inputs():
    """ function to update inputs read from the settings screen"""
    global update_interval, temp_alarm_lim,Phone_Num,PhProvider,email,phoneCompanies
    temp_alarm_lim=int(ui.AlarmLimitIn.text())
    update_interval=int(ui.RefreshDelIn.text())
    Phone_Num=ui.PhNoIn.text()
    alarm_check()
    PhProvider=ui.phCoIn.currentText()
    email=Phone_Num+phoneCompanies[PhProvider]
    #print(update_interval)
    
def alarm_check(): 
    """Check for alarm condition"""
    global temp_alarm_lim,temperature,temp_alarm,unit
    if((unit==1 and temperature>(int(sensorRead.todegF(temp_alarm_lim)))) 
    or (unit==0 and temperature>int(temp_alarm_lim))):
        set_alarm()
    elif((unit==1 and temperature<(int(sensorRead.todegF(temp_alarm_lim-1)))) 
    or (unit==0 and temperature<int(temp_alarm_lim)-1)):
        reset_alarm()
        
def set_alarm():
    """Set the alarm to 1 and change colour of LCD to red"""
    global messageSent,temp_alarm,email
    ui.lcd_temperature.setStyleSheet("QLCDNumber{\n"
"    color: rgb(0, 0, 0);    \n"
"    background-color: rgb(255, 0, 0);\n"
"}")
    temp_alarm=1
    print("\nTemperature In Alarm \n")
    if(messageSent==0):
        SendMessage(email)
    
    
def reset_alarm():
    """reset alarm to 0 and change back colour of LCD"""
    global temp_alarm,messageSent
    temp_alarm=0
    messageSent=0
    ui.lcd_temperature.setStyleSheet("QLCDNumber{\n"
"    color: rgb(0, 0, 0);    \n"
"    background-color: rgb(170, 255, 255);\n"
"}")
    print("\nNo Temperature Alarm")
    
def SendMessage(email):
    """function to send email/message"""
    global messageSent,temperature
    
    from_email = Email("alarms@HomeRasPi.com")
    to_email = Email(email)
    subject = "***Temperature in Alarm***"
    content = Content("text/plain", "The monitored Temperature is "+str(temperature))
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
    messageSent=1
    print("Message sent to ",email)
    
update_data()
update_Inputs()
ui.pushButton_Refresh.clicked.connect(lambda:update_data())
ui.radioButton_degF.clicked.connect(lambda:change_to_degF())
ui.radioButton_degC.clicked.connect(lambda:change_to_degC())
ui.saveButton.clicked.connect(lambda:update_Inputs())

sys.exit(app.exec_())

