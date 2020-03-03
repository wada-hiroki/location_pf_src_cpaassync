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
import viewtable

class Organization():
	def __init__(self, config, log):
		# set config
		self.api_retry_threshold = int(config['hr']['api_retry_threshold'])
		self.api_msleep_time = int(config['hr']['api_msleep_time'])
		self.db_retry_threshold = int(config['hr']['db_retry_threshold'])
		self.db_msleep_time = int(config['hr']['db_msleep_time'])

		# set logger
		self.log = json.loads(log['organization']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)

		# set object
		self.coop = cooperation.Cooperation(config,log)
		self.locationpf = locationpf.LocationPf(config, log)
		self.view = viewtable.Viewtable(config, log)


	# set data insert into t_organizations_sync
	def format_db_data(self, data):
		return {\
				"CN": data[14],\
				"COMPANY_CD": data[0],\
				"ORGANIZATION_CD": data[7],\
				'UPDATE_DATE': '',\
				"SYNC_RESULT": 0,\
				"SYNC_TIME": "",\
				"SYNC_FAIL_REASON": ""\
			}


	# Set post request body
	def format_request_body(self, data):
		return {\
				"companyCd": data[0],\
				"companyName": data[1],\
				"organizationCd": data[7],\
				"organizationName": data[9],\
				"organizationCd1": data[7],\
				"organizationName1": data[9],\
				"organizationCd2": data[7],\
				"organizationName2": data[9],\
				"organizationCd3": data[7],\
				"organizationName3": data[9],\
				"organizationLevel": data[12]\
			}


	def delete(self, organization, nowtime):
		# set function name
		func_name = sys._getframe().f_code.co_name
		unique_cd = organization[14]
		date = organization[6]
		update_date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00:00.000000'

		# do not delete if abolition_date is newer than nowtime
		if datetime.datetime.strptime(update_date, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		#if update_date > nowtime:
			return True

		# set data insert into t_organizations_sync
		data = self.format_db_data(organization)
		data['UPDATE_DATE'] = update_date

		# connect to cooperation database
		self.coop.connect_db()

		# set uri parameter
		uri = {\
				'companyCd': organization[0],\
				'organizationCd': organization[7]\
			}

		# delete organization from location platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.delete_organization(uri):
				logger.info(self.log['260000'], func_name, unique_cd)
				break
			else:
				logger.warning(self.log['360001'], func_name, unique_cd, (i+1))
				usleep(self.api_msleep_time * 1000)

		# output error log if faild delete organization from location platform
		if i == (self.api_retry_threshold - 1):
			data['SYNC_RESULT'] = 1
			data['SYNC_FAIL_REASON'] =\
					"Faild delete organization from Location Platform"
			logger.error(self.log['460001'], func_name, unique_cd)
			for i in range(self.db_retry_threshold):
				# update fail reason to t_organizations_sync
				if self.coop.update_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					break
				else:
					logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild update organization to t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# update t_organizations_sync set delete organization result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.update_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					break
				else:
					logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild update organization to t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# commit cooperation database
		self.coop.commit_db()
		# close cooperation database
		self.coop.close_db()

		return True


	def regist(self, organization, nowtime):
		# set function name
		func_name = sys._getframe().f_code.co_name
		unique_cd = organization[14]
		date = organization[5]
		update_date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00:00.000000'

		# do not delete if abolition_date is newer than nowtime
		if datetime.datetime.strptime(update_date, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		#if datetime.datetime.strptime(update_date, '%Y-%m-%d 00:00:00.000000') > nowtime:
		#if update_date > nowtime:
			return True

		# connect to cooperation database
		self.coop.connect_db()

		# set post request body
		body = self.format_request_body(organization)
		org_cd = organization[7]
		tmp_cd_list = []
		tmp_cd_list = org_cd.split('-')
		org_cd_list = []
		for i in range(len(tmp_cd_list)):
			if i == 0:
				org_cd_list.append(tmp_cd_list[i])
			else:
				org_cd_list.append(org_cd_list[i-1] + '-' + tmp_cd_list[i])
		org_name_list = []
		for cd in org_cd_list:
			org_name_list.append(self.view.select_organization_name_by_cd(cd))

		# set data insert into t_organizations_sync
		data = self.format_db_data(organization)
		data['UPDATE_DATE'] = update_date

		# post organization to location platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.post_organization(body):
				logger.info(self.log['260001'], func_name, unique_cd)
				break
			else:
				logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
				usleep(self.api_msleep_time * 1000)

		# output error log if faild regist organization of location platform
		if i == (self.api_retry_threshold - 1):
			data['SYNC_RESULT'] = 1
			data['SYNC_FAIL_REASON'] =\
					"Faild regist organization to Location Platform"
			logger.error(self.log['460002'], func_name, unique_cd)
			for i in range(self.db_retry_threshold):
				# insert organization into t_organizations_sync
				if self.coop.insert_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					# Commit cooperation database
					self.coop.commit_db()
					# Close cooperation database
					self.coop.close_db()
					return False
				else:
					logger.warning(self.log['360002'], func_name,  unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild insert organization into t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# update t_organizations_sync set post organization result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.update_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					break
				else:
					logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild update organization to t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.close_db()
				return False

		# commit cooperation database
		self.coop.commit_db()
		# close cooperation database
		self.coop.close_db()

		return True


	def update(self, organization, nowtime):
		# set function name
		func_name = sys._getframe().f_code.co_name
		unique_cd = organization[14]
		date = organization[15]
		update_date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00:00.000000'

		# do not delete if abolition_date is newer than nowtime
		if datetime.datetime.strptime(update_date, '%Y-%m-%d %H:%M:%S.%f') > nowtime:
		#if update_date > nowtime:
			return True

		# connect to cooperation database
		self.coop.connect_db()

		# Set URI parameter
		uri = {\
				'companyCd': organization[0],\
				'organizationCd': organization[7]\
			}

		# set post request body
		body = self.format_request_body(organization)

		# set data update to t_organizations_sync
		data = self.format_db_data(organization)
		data['UPDATE_DATE'] = update_date

		# update organization to location platform
		for i in range(self.api_retry_threshold):
			data['SYNC_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			if self.locationpf.patch_organization(uri, body):
				logger.info(self.log['260001'], func_name, unique_cd)
				break
			else:
				logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
				usleep(self.api_msleep_time * 1000)

		# output error log if faild update organization of location platform
		if i == (self.api_retry_threshold - 1):
			data['SYNC_RESULT'] = 1
			data['SYNC_FAIL_REASON'] =\
					"Faild update organization to Location Platform"
			logger.error(self.log['460002'], func_name, unique_cd)
			for i in range(self.db_retry_threshold):
				# insert organization into t_organizations_sync
				if self.coop.update_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					# Commit cooperation database
					self.coop.commit_db()
					# Close cooperation database
					self.coop.close_db()
					return False
				else:
					logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild update organization into t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.rollback_db()
				self.coop.close_db()
				return False

		# update t_organizations_sync set post organization result
		else:
			for i in range(self.db_retry_threshold):
				if self.coop.update_organization(data):
					logger.info(self.log['260004'], func_name, unique_cd)
					break
				else:
					logger.warning(self.log['360002'], func_name, unique_cd, (i+1))
					usleep(self.db_msleep_time * 1000)
			# output error log if faild update organization to t_organizations_sync
			if i == (self.db_retry_threshold - 1):
				logger.error(self.log['460003'], func_name, unique_cd)
				self.coop.close_db()
				return False

		# commit cooperation database
		self.coop.commit_db()
		# close cooperation database
		self.coop.close_db()

		return True
