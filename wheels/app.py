#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/20

__author__ = 'icejoywoo'

import web

urls = (
    '/', 'index'
)


class index:
    def GET(self):
        return 'Hello, World!'

app = web.application(urls, globals())
application = app.wsgifunc()

# python wsgi_server.py app:application
