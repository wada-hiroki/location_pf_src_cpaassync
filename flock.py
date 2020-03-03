#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import fcntl
import hashlib
import json
from loguru import logger

class Flock():
	def __init__(self, conf, log):
		# set config
		lock_dir = conf['flock']['lock_dir']
		file_name = conf['flock']['filename']
		salt = conf['flock']['salt']

		# set logger
		self.log = json.loads(log['flock']['log'])
		logfile = conf['logger']['logfile']
		rotation = conf['logger']['rotation']
		retention = int(conf['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)

		# set lockfile name
		self.lockfile =\
				lock_dir + hashlib.md5((file_name + salt).encode('utf-8')).hexdigest()


	def lock(self):
		func_name = sys._getframe().f_code.co_name
		with open(self.lockfile, "w") as fp:
			try:
				# Lock file
				fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
				logger.info(self.log['240000'], func_name, 'info')
				return True
			except IOError as e:
				logger.error(self.log['440000'], func_name)
				return False
			return True


	def unlock(self):
		func_name = sys._getframe().f_code.co_name
		try:
			# Unnlock
			fcntl.flock(self.fp, fcntl.LOCK_UN)
			logger.info(self.log['240000'], func_name, 'info')
			return True
		except IOError as e:
			logger.critical(self.log['540000'], func_name)
			return False

		self.fp.close()
		return True
