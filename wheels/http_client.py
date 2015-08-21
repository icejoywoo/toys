#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/20

__author__ = 'wujiabin'

import socket

HOST, PORT = 'localhost', 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.sendall("GET /hello HTTP/1.1\r\n\r\n")
print client_socket.recv(2014)
