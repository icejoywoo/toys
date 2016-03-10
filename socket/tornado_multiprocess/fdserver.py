#!/usr/bin/env python
"""This is a demonstration of sharing file descriptors across processes.

It uses Tornado (need a recent post-2.0 version from github) and the
multiprocessing module (from python 2.6+).  To run it, start one copy
of fdserver.py and one or more copies of testserver.py (in different
terminals, or backgrounded, etc).  Fetch http://localhost:8000 and
you'll see the requests getting answered by different processes (it's
normal for several requests to go to the same process under light
load, but under heavier load it tends to even out).

This approach offers a third way to build multi-process tornado apps
(in addition to independent processes balanced by e.g. nginx, or
tornado's built-in multi-process mode).

Compared to tornado's fork_processes, this approach is slightly more
complex due to the addition of fdserver (and because the processes are
started independently you'll probably want a process manager like
supervisord), but allows you to do graceful rolling restarts without
taking the entire group of processes down at once.

Compared to putting tornado processes behind nginx, this approach is
simpler (since fdserver is much simpler than configuring
nginx/haproxy) and avoids issues with ephemeral port limits that can
be a problem in high-traffic proxied services.  However, exposing
tornado to the world without a proxy is somewhat more vulnerable to
DoS attacks, so I still recommend a proxy for high-traffic sites unless
there is specific evidence that removing the proxy will help.

This technique can also be used for privilege separation: you can run
fdserver as root so it can bind to port 80, and then (with the unix
socket chown/chmod'ed appropriately) run the rest of the app as an
unprivileged user.
"""

import errno
import socket

from multiprocessing.reduction import send_handle

from tornado.options import define, options, parse_command_line
from tornado.netutil import bind_sockets, bind_unix_socket
from tornado.ioloop import IOLoop

define('port', default=8000)
define('unix_socket', default='/tmp/fdserver.sock')

def main():
    parse_command_line()

    # restrict to ipv4 so we only get one socket back
    tcp_sockets = bind_sockets(options.port, family=socket.AF_INET)
    assert len(tcp_sockets) == 1
    tcp_socket = tcp_sockets[0]

    unix_socket = bind_unix_socket(options.unix_socket)

    def handle_connection(fd, events):
        while True:
            try:
                connection, address = unix_socket.accept()
            except socket.error, e:
                if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return
                raise
            send_handle(connection, tcp_socket.fileno(),
                        None  # destination_pid not needed on unix
                        )
            connection.close()

    IOLoop.instance().add_handler(unix_socket.fileno(), handle_connection,
                                  IOLoop.READ)

    IOLoop.instance().start()

if __name__ == '__main__':
    main()
