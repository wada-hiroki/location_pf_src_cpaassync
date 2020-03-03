#!/usr/bin/env python3
# coding: utf-8
import sys
import os
import configparser
import datetime
import time
import json
from loguru import logger

import flock
import hr

def main():
	func_name = sys._getframe().f_code.co_name

	# Load config
	config_ini = configparser.ConfigParser()
	config_ini.read('conf/config.ini', encoding='utf-8')

	os.environ['HTTP_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
	os.environ['HTTPS_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
	os.environ['NLS_LANG'] = 'Japanese_Japan.AL32UTF8'

	# Set logger
	log_ini = configparser.ConfigParser()
	log_ini.read('conf/log.ini', encoding='utf-8')
	log = log_ini['sync_hr']
	logfile = config_ini['logger']['logfile']
	rotation = config_ini['logger']['rotation']
	retention = int(config_ini['logger']['retention'])
	logger.remove()
	logger.add(logfile, rotation=rotation, retention=retention)

	# Set flock object
	flock_obj = flock.Flock(config_ini, log_ini)

	# Get nowtime
	nowtime = datetime.datetime.now()

	# Exclusive lock
	if not flock_obj.lock():
		logger_obj.warning(log['300000'], func_name)
		sys.exit()

	# Synchronized human resources
	hr_obj = hr.Hr(config_ini, log_ini)

	# Get nowtime
	nowtime = datetime.datetime.now()

	# Update employees
	hr_obj.update_employees(nowtime)

	# Update organizations
	hr_obj.update_organizations(nowtime)

	# Unlock
	flock_obj.unlock()

	# Exit main
	sys.exit()


main()
