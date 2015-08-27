#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/8/26

__author__ = 'wujiabin'

import logging
import sys

from structlog import getLogger, wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level


logger = getLogger('hello.logger')

logger = logger.bind(user='anonymous', some_key=23)
logger.info('user.logged_in', happy=True)

logger = logger.bind(user='hynek', some_key=42)
logger.info('user.logged_in', happy=True, num_list=[1, 2, 3])


# json log
logging.basicConfig(stream=sys.stdout, format='%(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
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
