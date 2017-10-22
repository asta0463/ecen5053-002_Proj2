""""
ECEN5053-002 Project2
server.py
code to setup tornado web server

"""
import tornado.ioloop
import tornado.web
import databaseOps

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class getData(tornado.web.RequestHandler):
    def get(self):
        h,t=databaseOps.getData()
        self.write("Humidity ",h," ","Temperature ",t)
        print(h," ",t)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

application = tornado.web.Application([
    (r"/getdata",getData),    
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])    
   
    
if __name__ == "__main__":
    #app = make_app()
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
    