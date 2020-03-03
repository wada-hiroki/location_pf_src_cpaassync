#!/usr/bin/env python3
# coding: utf-8
import sys
import datetime
import json
import time
usleep = lambda x: time.sleep(x/1000000.0)
from loguru import logger

import cooperation
import locationpf


class Employee():
	def __init__(self, config, log):
		# Set config
		self.api_retry_threshold = int(config['hr']['api_retry_threshold'])
		self.api_msleep_time = int(config['hr']['api_msleep_time'])
		self.db_retry_threshold = int(config['hr']['db_retry_threshold'])
		self.db_msleep_time = int(config['hr']['db_msleep_time'])

		# set logger
		self.log = json.loads(log['employee']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)

		# Set object
		self.coop = cooperation.Cooperation(config, log)
		self.locationpf = locationpf.LocationPf(config, log)


	# Set data insert into T_EMPLOYEES_SYNC
	def format_db_data(self, data):
		return {\
				"EMAIL_ADDRESS": data[0],\
				"DATA_UPD_TIME": data[18],\
				"SYNC_RESULT": 0,\
				"SYNC_TIME": "",\
				"SYNC_FAIL_REASON": ""\
			}


	# Set post request body
	def format_request_body(self, data):
		return {\
				"emailAddress": data[0],\
				"lastName": data[1],\
				"firstName": data[2],\
				"companyCd": '113305',\
				"organizationCd": data[8],\
				"presense": 0,\
				"enabled": 1\
			}


	def delete(self, employee, nowtime):
		# Set function name
		func_name = sys._getframe().f_code.co_name
		email = employee[0]
		del_time = employee[18]

		# date type check
		if type(del_time) is not datetime.datetime:
			logger.warning(self.log['350000'], func_name, email, del_time)
			return False

		# Do not delete if DATA_DEL_DATE is newer than nowtime
		#if datetime.datetime.strptime(del_time, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		if del_time > nowtime:
			return True

		# Connect to cooperation database
		self.coop.connect_db()

		# Set data insert into T_EMPLOYEES_SYNC
		data = self.format_db_data(employee)

		# Set URI Prameter
		uri = {\
				'emailAddress': email\
			}
		body = uri

		# Delete employee from Location Platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.delete_employee(uri, body):
				logger.info(self.log['250000'], func_name, email)
				break
			else:
				logger.warning(self.log['350001'], func_name, email, (i+1))
				usleep(self.api_msleep_time * 1000)

		# Output error log if faild delete employee from Location Platform
		if i == (self.api_retry_threshold - 1):
			# Update fail reason to T_EMPLOYEES_SYNC
			data['SYNC_RESULT'] = 1
			data['SYNC_FAIL_REASON'] =\
					"Faild delete employee from Location Platform"
			logger.error(self.log['450001'], func_name, email)
			for i in range(self.db_retry_threshold):
				if self.coop.update_employee(data):
					logger.info(self.log['250004'], func_name, email)
					# Commit cooperation database
					self.coop.commit_db()
					# Close cooperation databaase
					self.coop.close_db()
					return False
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild update employee to T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450003'], func_name, email)
				# Rollback cooperation database
				self.coop.rollback_db()
				# Close cooperation database
				self.coop.close_db()
				return False

		# Update T_EMPLOYEES_SYNC set delete employee result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.update_employee(data):
					logger.info(self.log['250004'], func_name, email)
					break
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild update employee to T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450003'], func_name, email)
				# Rollback cooperation database
				self.coop.rollback_db()
				# Close cooperation database
				self.coop.close_db()
				return False

		# Commit cooperation database
		self.coop.commit_db()
		# Close cooperation database
		self.coop.close_db()

		return True


	def regist(self, employee, nowtime):
		# Set function name
		func_name = sys._getframe().f_code.co_name
		email = employee[0]
		reg_time = employee[16]

		# date type check
		if type(reg_time) is not datetime.datetime:
			logger.warning(self.log['350000'], func_name, email, reg_time)
			return False

		# Do not post if delete_time is newer than nowtime
		#if datetime.datetime.strptime(reg_time, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		if reg_time > nowtime:
			return True

		# Connect to cooperation database
		self.coop.connect_db()

		# Set post request body
		body = self.format_request_body(employee)

		# Set data insert into T_EMPLOYEES_SYNC
		data = self.format_db_data(employee)
		data['DATA_UPD_TIME'] = reg_time

		# Post employee to Location Platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.post_employee(body):
				logger.info(self.log['250001'], func_name, email)
				break
			else:
				logger.warning(self.log['350002'], func_name, email, (i+1))
				usleep(self.api_msleep_time * 1000)

		# Output error log if faild post employee of Location Platform
		if i == (self.api_retry_threshold - 1):
			# Insert employee into T_EMPLOYEES_SYNC
			data['SYNC_RESULT'] = 1
			data['SYNC_FAIL_REASON'] =\
					"Faild regist employee to Location Platform"
			logger.error(self.log['450002'], func_name, email)
			for i in range(self.db_retry_threshold):
				if self.coop.insert_employee(data):
					logger.info(self.log['250003'], func_name, email)
					break
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild insert employee into T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450004'], func_name, email)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# Update T_EMPLOYEES_SYNC set post employee result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.insert_employee(data):
					logger.info(self.log['250003'], func_name, email)
					# Commit cooperation database
					self.coop.commit_db()
					# Close cooperation databaase
					self.coop.close_db()
					return False
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild update employee to T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450003'], func_name, email)
				self.coop.close_db()
				return False

		# Commit cooperation database
		self.coop.commit_db()
		# Close cooperation database
		self.coop.close_db()

		return True


	def update(self, employee, nowtime):
		# Set function name
		func_name = sys._getframe().f_code.co_name
		email = employee[0]
		upd_time = employee[17]

		# date type check
		if type(upd_time) is not datetime.datetime:
			logger.warning(self.log['350000'], func_name, email, upd_time)
			return False

		# Do not post if DATA_UPD_DATE is newer than nowtime
		#if datetime.datetime.strptime(upd_time, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		if upd_time > nowtime:
			return True

		# Connect to cooperation database
		self.coop.connect_db()

		# Set post request body
		body = self.format_request_body(employee)

		# Set data update to T_EMPLOYEES_SYNC
		data = self.format_db_data(employee)
		data['DATA_UPD_TIME'] = upd_time

		# Set URI Prameter
		uri = {\
				'emailAddress': email\
			}

		# Post employee to Location Platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.patch_employee(uri, body):
				logger.info(self.log['250001'], func_name, email)
				break
			else:
				logger.warning(self.log['350002'], func_name, email, (i+1))
				usleep(self.api_msleep_time * 1000)

		# Output error log if faild post employee of Location Platform
		if i == (self.api_retry_threshold - 1):
			logger.error(self.log['450002'], func_name, email)
			for i in range(self.db_retry_threshold):
				# Insert employee into T_EMPLOYEES_SYNC
				data['SYNC_RESULT'] = 1
				data['SYNC_FAIL_REASON'] =\
						"Faild update employee to Location Platform"
				if self.coop.update_employee(data):
					logger.info(self.log['250004'], func_name, email)
					# Commit cooperation database
					self.coop.commit_db()
					# Close cooperation databaase
					self.coop.close_db()
					return False
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild update employee to T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450003'], func_name, email)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# Update T_EMPLOYEES_SYNC set update employee result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.update_employee(data):
					logger.info(self.log['250004'], func_name, email)
					break
				else:
					logger.warning(self.log['350002'], func_name, email, (i+1))
					usleep(self.db_msleep_time*1000)
			# Output error log if faild update employee to T_EMPLOYEES_SYNC
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['450003'], func_name, email)
				self.coop.close_db()
				return False

		# Commit cooperation database
		self.coop.commit_db()
		# Close cooperation database
		self.coop.close_db()

		return True
