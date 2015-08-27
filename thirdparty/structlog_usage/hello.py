#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/26

__author__ = 'wujiabin'

import logging
import logging.handlers
import os
import sys

from structlog import getLogger, wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level

# simple usage
logger = getLogger('hello.logger')

logger = logger.bind(user='anonymous', some_key=23)
logger.info('user.logged_in', happy=True)

logger = logger.bind(user='hynek', some_key=42)
logger.info('user.logged_in', happy=True, num_list=[1, 2, 3])


# json log
logging.basicConfig(stream=sys.stdout, format='%(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s %(threadName)s %(lineno)d %(levelname)s %(message)s'
log_dir = os.path.join(os.path.dirname(__file__), "log")
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
fa = logging.handlers.RotatingFileHandler(os.path.join(log_dir, "test.log"), 'a', 20*1024*1024, 2)
fa.setLevel(logging.DEBUG)
fa.setFormatter(logging.Formatter(FORMAT))
_logger.addHandler(fa)

logger = wrap_logger(
    _logger,
    processors=[
        filter_by_level,
        JSONRenderer(),  # JSONRenderer(indent=1, sort_keys=True),
    ]
)

logger = logger.bind(user='anonymous', some_key=23)
logger.info('user.logged_in', happy=True)

logger = logger.bind(user='hynek', some_key=42)
logger.info('user.logged_in', happy=True, num_list=[1, 2, 3])
