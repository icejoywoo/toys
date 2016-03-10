#!/usr/bin/env python

import os
import socket

from multiprocessing.reduction import recv_handle

from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

define('unix_socket', default='/tmp/fdserver.sock')

class HelloHandler(RequestHandler):
    def get(self):
        self.write("Hello from %d\n" % os.getpid())

def main():
    parse_command_line()

    unix_socket = socket.socket(socket.AF_UNIX)
    unix_socket.connect(options.unix_socket)

    fd = recv_handle(unix_socket)
    app = Application([('/', HelloHandler)])
    server = HTTPServer(app)
    server.add_socket(socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM))

    IOLoop.instance().start()

if __name__ == "__main__":
    main()
