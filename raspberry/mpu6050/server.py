#!/usr/bin/python
# sudo apt-get install python-webpy

import web
import mpu6050

urls =('/', 'index')

class WebService(web.application):
    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class index(object):

  def __init__(self):
    self.mpu = mpu6050.Sensor()
    self.render=web.template.render('templates/')
 
  def GET(self):
    return self.render.index(self.mpu.temperature())

if __name__ == "__main__":
  app = WebService(urls, globals())
  app.run()

