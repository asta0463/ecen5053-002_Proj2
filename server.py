import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options

import json
import socket
import databaseOps as dbop

unit=0 # 1 is degF and 0 is degC

dbop.addDataToDb()

def changeToC():
    global unit
    unit=0

def changeToF():
    global unit
    unit=1

class WSHandler(tornado.websocket.WebSocketHandler):
    global unit
    def open(self):
        print ('new connection')
        self.write_message(dbop.ws_cur_data(unit))   
        self.write_message(dbop.ws_last_temp(unit))
        self.write_message(dbop.ws_avg_temp(unit))
        self.write_message(dbop.ws_max_temp(unit))
        self.write_message(dbop.ws_min_temp(unit))
        self.write_message(dbop.ws_last_hum())
        self.write_message(dbop.ws_avg_hum())
        self.write_message(dbop.ws_max_hum())
        self.write_message(dbop.ws_min_hum())
      
    def on_message(self, message):
        print ('request for  %s' % message)
        
        if(message=='cur_data'):
            self.write_message(dbop.ws_cur_data(unit))
        elif(message=='last_temp'):    
            self.write_message(dbop.ws_last_temp(unit))
        elif(message=='avg_temp'):    
            self.write_message(dbop.ws_avg_temp(unit))    
        elif(message=='max_temp'):    
            self.write_message(dbop.ws_max_temp(unit))    
        elif(message=='min_temp'):    
            self.write_message(dbop.ws_min_temp(unit))    
        elif(message=='last_hum'):
            self.write_message(dbop.ws_last_hum())
        elif(message=='avg_hum'):
            self.write_message(dbop.ws_avg_hum())       
        elif(message=='max_hum'):
            self.write_message(dbop.ws_max_hum())     
        elif(message=='min_hum'):
            self.write_message(dbop.ws_max_hum())             
        elif(message=='C'):    
            changeToC()
            print(unit)
            self.write_message(dbop.ws_cur_data(unit))   
            self.write_message(dbop.ws_last_temp(unit))
            self.write_message(dbop.ws_avg_temp(unit))
            self.write_message(dbop.ws_max_temp(unit))
            self.write_message(dbop.ws_min_temp(unit)) 
        elif(message=='F'):    
            changeToF()
            print(unit)
            self.write_message(dbop.ws_cur_data(unit))   
            self.write_message(dbop.ws_last_temp(unit))
            self.write_message(dbop.ws_avg_temp(unit))
            self.write_message(dbop.ws_max_temp(unit))
            self.write_message(dbop.ws_min_temp(unit))     
            
 
    def on_close(self):
        print ('connection closed')
 
    def check_origin(self, origin):
        return True

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html') 

class StaticFileHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('main.js')
    
application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r"/", IndexHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {'path':  './'}),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    myIP = socket.gethostbyname(socket.gethostname())
    print( '*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start() 

