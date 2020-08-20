#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
from common.conf import crm_cfg

log_level = {
	'ERROR': logging.ERROR,
	'WARNING': logging.WARNING,
	'INFO': logging.INFO,
	'DEBUG': logging.DEBUG
}

logger = logging.getLogger('hcrm-run')
logger.setLevel(level = log_level[crm_cfg['log']['level']])
formatter = logging.Formatter('%(asctime)s|%(filename)s|%(lineno)d|%(levelname)s|%(message)s')
handler = TimedRotatingFileHandler(filename = crm_cfg['log']['path']+'run.log', when="D", interval=1, backupCount=30)
handler.setFormatter(formatter)
logger.addHandler(handler)


conf_formatter = logging.Formatter('%(asctime)s|%(filename)s|%(lineno)d|%(levelname)s|%(message)s')
conf_handler = TimedRotatingFileHandler(filename = crm_cfg['log']['path']+'conf.log', when="D", interval=1, backupCount=30)
conf_handler.setFormatter(conf_formatter) 
conf_logger = logging.getLogger('hcrm-conf')
conf_logger.setLevel(level = log_level[crm_cfg['log']['level']])
conf_logger.addHandler(conf_handler)
