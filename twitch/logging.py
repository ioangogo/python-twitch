# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import logging
import copy

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


def _mask(message):
    mask = '*' * 11
    masked_message = re.sub(r'((?:OAuth|Bearer)\s)[^\'"]+', r'\1' + mask, message)
    masked_message = re.sub(r'(["\']email["\']:\s*[\'"])[^\'"]+', r'\1' + mask, masked_message)
    masked_message = re.sub(r'(USER-IP=[\'"])[^\'"]+', r'\1' + mask, masked_message)
    masked_message = re.sub(r'(["\']client_secret["\']:\s*[\'"])[^\'"]+', r'\1' + mask, masked_message)
    masked_message = re.sub(r'(client_secret=).+?(&|$|\|)', r'\1' + mask + r'\2', masked_message)
    return masked_message


def _add_leader(message):
    return message


def prep_log_message(message):
    message = copy.deepcopy(message)
    message = _mask(message)
    message = _add_leader(message)
    return message


class Log:
    def __init__(self):
        self._log = logging.getLogger('twitch')
        self._log.addHandler(NullHandler())

    def info(self, message):
        message = prep_log_message(message)
        self._log.info(message)

    def debug(self, message):
        message = prep_log_message(message)
        self._log.debug(message)

    def warning(self, message):
        message = prep_log_message(message)
        self._log.debug(message)

    def error(self, message):
        message = prep_log_message(message)
        self._log.error(message)

    def critical(self, message):
        message = prep_log_message(message)
        self._log.critical(message)

    def deprecated_query(self, old, new):
        self.warning('DEPRECATED call to |{0}| detected, please use |{1}| instead'.format(old, new))

    def deprecated_api_version(self, old, new, eol_date):
        self.warning('API version |{0}| is deprecated, update to |{1}| by |{2}|'.format(old, new, eol_date))


log = Log()
