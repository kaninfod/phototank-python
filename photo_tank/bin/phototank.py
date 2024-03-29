#! /usr/bin/env python
__author__ = 'hingem'

from photo_tank.app import app
from photo_tank.bin.daemon import Daemon
import sys




class MyDaemon(Daemon):
    def run(self):
        app.logger.debug("Starting Tornado...")
        print('Tornado on port {port}...'.format(port=app.config['SERVER_PORT']))
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(app.config['SERVER_PORT'])
        IOLoop.instance().start()

if __name__ == "__main__":

    import os
    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
        print(user_paths)
    except KeyError:
        user_paths = []

    daemon = MyDaemon('/tmp/phomand.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)