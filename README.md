# ecen5053-002_Proj2
Project 2 for Embedded Interface Design

///// Sensor RPI3

temp sensor connected to rpi3 to take readings once every 5 seconds, and 
display in QT the last, average, highest, and lowest readings for both temp and 
humidity with time/date of each reading (total of eight timestamped values).

Ability to switch between, degC or degF.

RPi3 should store temp and humidity readings (with timestamps) in a local data store ,
possible tinydb or Redis. -- Figure out which one to use.

Sensor RPi3 should also run a web server to allow the remote RPi3 to request and display data –
Required to use websockets as the communication protocol between the sensor RPi3 and the remote display RPi3
-- Tornado looks good.

Stretch Goal - Ability to switch between timezones.


///////////////// REMOTE RPI3
The remote display should be developed as an HTML/jQuery web page that will run on the remote RPi3
--- Check if fantom is a possibility here. It may solve some UI issues etc.
and talk to the sensor RPi3’s webserver to request data for display
 
The webpage should:
Connect to the sensor RPi3 webserver via websockets
Indicate any error conditions
Provide eight buttons to request and display:
Last temp or humidity reading with timestamp
Average temp or humidity reading w/timestamp
Lowest temp or humidity reading w/timestamp
Highest temp or humidity reading w/timestamp


---------
Suggested Extra Credit Items
HTTPS secure client/server connection
Graphing of data on the web page
------------------

Stretch Goals
Security HTTPS, instead of HTTP.
Security, OAuth Login -- Possibilities in tornado
Data Graphing in HTML, not on the QT framework. -- Possibility of embedding numpy graphs in HTML ?
Ability to switch an output, once security is done. This should be a possibility.
If output switches, then a full thermostat can be made. May be seperate UI for it.








