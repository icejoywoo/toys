#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/20

__author__ = 'wujiabin'


def app(environ, start_response):
    """A barebones WSGI application.

    This is a starting point for your own Web framework :)
    """
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world from a simple WSGI application!\n']
