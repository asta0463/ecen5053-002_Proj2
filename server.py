""""
ECEN5053-002 Project2
server.py
code to setup tornado web server

"""
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

application = tornado.web.Application([
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])    
   
    
if __name__ == "__main__":
    #app = make_app()
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
    