#!/usr/bin/env python
# ^_^ encoding: utf-8 ^_^
# Copyright 2012 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
""" Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
Tornado 的日志模块，稍作修改，作为简单通用的日志模块, 适用于 Python2.7.x
日志分为两个文件: .log.wf是warning以上级别的日志, .log是包含配置的所有级别的日志

@author: tornado
@author: icejoywoo
"""
from __future__ import absolute_import, division, print_function, with_statement
import logging
import logging.handlers
import sys
import os

__all__ = ['LogFormatter', 'enable_pretty_logging', 'setup_logger']

unicode_type = unicode
bytes_type = str
basestring_type = str

try:
    import curses
except ImportError:
    curses = None


def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


def safeunicode(obj, encoding='utf-8'):
    r"""s
    Converts any given object to unicode string.

        >>> safeunicode('hello')
        u'hello'
        >>> safeunicode(2)
        u'2'
        >>> safeunicode('\xe1\x88\xb4')
        u'\u1234'
    """
    t = type(obj)
    if t is unicode:
        return obj
    elif t is str:
        return obj.decode(encoding, 'ignore')
    elif t in [int, float, bool]:
        return unicode(obj)
    elif hasattr(obj, '__unicode__') or isinstance(obj, unicode):
        try:
            return unicode(obj)
        except Exception:
            return u""
    else:
        return str(obj).decode(encoding, 'ignore')


def _safe_unicode(s):
    try:
        return safeunicode(s)
    except UnicodeDecodeError:
        return repr(s)


class LogFormatter(logging.Formatter):
    """Log formatter used in Tornado.

    Key features of this formatter are:

    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.

    This formatter is enabled automatically by
    `tornado.options.parse_command_line` (unless ``--logging=none`` is
    used).
    """
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s.%(msecs)03d ' \
            '%(filename)s:%(module)s:%(lineno)d %(process)d:%(thread)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y-%m-%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG:      4,  # Blue
        logging.INFO:       2,  # Green
        logging.WARNING:    3,  # Yellow
        logging.ERROR:      1,  # Red
    }

    def __init__(self, color=True, fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.

        .. versionchanged:: 3.2

           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt

        self._colors = {}
        if color and _stderr_supports_color():
            # The curses module has some str/bytes confusion in
            # python3.  Until version 3.2.3, most methods return
            # bytes, but only accept strings.  In addition, we want to
            # output these strings with the logging module, which
            # works with unicode strings.  The explicit calls to
            # unicode() below are harmless in python2 but will do the
            # right conversion in python 3.
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")

            for levelno, code in self.DEFAULT_COLORS.items():
                self._colors[levelno] = unicode_type(curses.tparm(fg_color, code), "ascii")
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")
        else:
            self._normal = ''

    def format(self, record):
        try:
            message = record.getMessage()

            # in uts, use the super good safeunicode function is just ok, no assert needed

            # ###  Below is the original notes from tornado  ###
            # assert isinstance(message, basestring_type)  # guaranteed by logging
            # Encoding notes:  The logging module prefers to work with character
            # strings, but only enforces that log messages are instances of
            # basestring.  In python 2, non-ascii bytestrings will make
            # their way through the logging framework until they blow up with
            # an unhelpful decoding error (with this formatter it happens
            # when we attach the prefix, but there are other opportunities for
            # exceptions further along in the framework).
            #
            # If a byte string makes it this far, convert it to unicode to
            # ensure it will make it out to the logs.  Use repr() as a fallback
            # to ensure that all byte strings can be converted successfully,
            # but don't do it by default so we don't add extra quotes to ascii
            # bytestrings.  This is a bit of a hacky place to do this, but
            # it's worth it since the encoding errors that would otherwise
            # result are so useless (and tornado is fond of using utf8-encoded
            # byte strings whereever possible).

            record.message = _safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to _safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(_safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def enable_pretty_logging(level, log_file_prefix, logger=None, backupCount=10,
                          maxBytes=10000000, log_to_stderr=True):
    """ Turns on formatted logging output as configured.
        在setup_default_logger中呗调用
        log_to_stderr是否打印日志到stderr终端上
    """
    if logger is None:
        logger = logging.getLogger()
    logger.setLevel(level)
    channel = logging.handlers.RotatingFileHandler(
        filename=log_file_prefix,
        maxBytes=maxBytes,
        backupCount=backupCount)
    channel.setFormatter(LogFormatter(color=False))
    logger.addHandler(channel)

    wf_channel = logging.handlers.RotatingFileHandler(
        filename="%s.wf" % log_file_prefix,
        maxBytes=maxBytes,
        backupCount=backupCount)
    wf_channel.setFormatter(LogFormatter(color=False))
    wf_channel.setLevel(logging.WARNING)
    logger.addHandler(wf_channel)

    if (log_to_stderr or
            (log_to_stderr is None and not logger.handlers)):
        # Set up color if we are in a tty and curses is installed
        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter())
        logger.addHandler(channel)


def setup_logger(logger, workspace='.', level=logging.DEBUG, log_to_stderr=True):
    """
    The helper function to create logger
    """
    import time
    log_path = os.path.join(workspace, 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, "%s.%s.%s.log" % (logger.name, int(time.time()), os.getpid()))
    enable_pretty_logging(level, log_file, logger, log_to_stderr=log_to_stderr)
    return log_file

# sqlalchemy logging config for compacity
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
