#!/usr/bin/python
"""
Simple Web application
Requires:
sudo apt-get install python-webpy
"""

import json
import web
import mpu6050

_URLS = ('/', 'Index', '/json/(.*)', 'HandleJSON')
_MPU = mpu6050.Sensor()
_RENDER = web.template.render('templates/')

class WebService(web.application):
    """
    Simple Web application
    """
    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class HandleJSON(object):
    """ 
      JSON handler
    """
    def GET(self, res):
        """
        Callback method handling HTTP GET request
        """
        web.header('Content-Type', 'application/json')
        return json.dumps({ field : value for field, value in zip(("x","y","z","t"), _MPU.data()) })

class Index(object):
    """
      HTML Index
    """
    def GET(self):
        """
        Sends temperature in formated html
        """
        return _RENDER.index("%.02f" % _MPU.temperature())

if __name__ == "__main__":
    WebService(_URLS, globals()).run()
