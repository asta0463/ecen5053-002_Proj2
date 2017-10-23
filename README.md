Aakash Kumar

###Project 2 of ECEN-5053-002 Embedded Interface Design 
Temperature Sensor Interface with Raspberry Pi and UI using QT Ability to switch between degF and degC values Auto refresh of values at user defined periods
Using websockets to let another pi view the data collected on the sensor pi

##Installation Instructions 
*Clone github repository from https://github.com/aakashpk/ecen5053-002_Proj2 
*The project uses sendgrid for emailing/messaging of alerts Install sendgrid python API using pip by running

*pip3 install sendgrid

*It requires use of tornado , can be installed by running if not already installed on the pi

*pip3 install tornado

*Uses tinydb as the database, can be installed by running 

*pip3 install tinydb 

##Run instructions
*The javascript used are from google APIs, the raspberry pi running this will require internet connection <return>
the websocket is setup for ip address 192.168.43.185 , this may have to be changed in the main.js file

*run server.py to start the websocket server and data collection in the database <return> 
to view GUI run the python file local.py

##Files in the directory
*index.html - base web page to be displayed
*main.js - javascript/jQuery being used in the webpage
*style.css - css style sheets for the webpage
*server.py - setup of websocket server and database and continuous data update
*sensorRead.py - hardware interface functions, reads values from the DHT sensor and GPIO setup, also takes care of unit conversion between degC and degF
*databaseOps.py - database operations and responses to tornado queries
*window_template.py - QT UI template file
*local.py - qt GUI program to display data


##Project Work --  Aakash Kumar - responsible for all parts

##Refferences

maximum calculation code from https://stackoverflow.com/questions/5320871/in-list-of-dicts-find-min-value-of-a-common-dict-field

2 column html css layout https://www.thesitewizard.com/css/design-2-column-layout.shtml

deg C deg F encoding https://stackoverflow.com/questions/10797686/best-way-to-encode-degree-celsius-symbol-into-web-page

radio button usage https://stackoverflow.com/questions/6654601/jquery-if-radio-button-is-checked

javascript splitting strings :https://stackoverflow.com/questions/3522406/javascript-split-string-straight-to-variables

sockets usage :http://blog.teamtreehouse.com/an-introduction-to-websockets
				http://fabacademy.org/archives/2015/doc/WebSocketConsole.html
				
javascript and html tutorials on w3schools.com				

basic usage of websockets https://os.mbed.com/cookbook/Websockets-Server









