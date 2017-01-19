from __future__ import print_function
import os, sys

import logging
import logging.config
logger = logging.getLogger('app.utils')

def setup_logging(level='INFO'):
  """Setup logging

  :param level: The level to set in the logging configuration
  """
  LOGGER_DEFAULT = {
    'level': level
  }
  LOG_CONFIG = {
    "version": 1,
   "formatters": {
     "default": {
       "format": "%(levelname)-8s %(module)s %(funcName)s - %(message)s",
       "datefmt": "%Y-%m-%d %H:%M:%S"
     },
    },
    "handlers": {
      "console": {
        "class": "logging.StreamHandler",
        "formatter": "default"
      },
    },
    "loggers": {
      "app.main": LOGGER_DEFAULT,
      "app.utils": LOGGER_DEFAULT,
      "app.project": LOGGER_DEFAULT,
    },
    "root": {
      "handlers": ["console"],
    },
  }
  logging.config.dictConfig(LOG_CONFIG)
