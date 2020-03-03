#!/usr/bin/env python3
# coding: utf-8
import sys
import json
import MySQLdb
from loguru import logger

class Cooperation():
	def __init__(self, config, log):
		# set config
		self.host = config['cooperation']['host']
		self.port = config['cooperation']['port']
		self.database = config['cooperation']['database']
		self.user = config['cooperation']['user']
		self.password = config['cooperation']['password']

		# set logger
		self.log = json.loads(log['cooperation']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)

	def connect_db(self):
		self.connection = MySQLdb.connect(\
				host=self.host,\
				user=self.user,\
				passwd=self.password,\
				db=self.database\
			)
		self.cursor = self.connection.cursor()
		return True

	def rollback_db(self):
		self.connection.rollback()

	def commit_db(self):
		self.connection.autocommit(False)
		self.connection.commit()

	def close_db(self):
		self.connection.close()

	def select_employee(self, email):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = 'select * from T_EMPLOYEES_SYNC where EMAIL_ADDRESS = %s'
			self.cursor.execute(sql, [email])
			logger.info(self.log['230000'], func_name, email)
			return self.cursor.fetchall()
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, email, e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, email, e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, email, e)
			return False


	def select_organization(self, cn):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = 'select * from T_ORGANIZATIONS_SYNC where CN = %s'
			self.cursor.execute(sql, [cn])
			logger.info(self.log['230000'], func_name, cn)
			return self.cursor.fetchall()
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, cn, e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, cn, e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, cn, e)
			return False


	def insert_employee(self, data):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec insert
			sql = 'insert into T_EMPLOYEES_SYNC '\
							'('\
								'EMAIL_ADDRESS,'\
								'DATA_UPD_TIME,'\
								'SYNC_RESULT,'\
								'SYNC_TIME,'\
								'SYNC_FAIL_REASON'\
							') '\
							'values (%s, %s, %s, %s, %s)'
			self.cursor.execute(sql, \
					[\
						data['EMAIL_ADDRESS'],\
						data['DATA_UPD_TIME'],\
						data['SYNC_RESULT'],\
						data['SYNC_TIME'],\
						data['SYNC_FAIL_REASON']\
					]\
				)
			logger.info(self.log['230000'], func_name, data['EMAIL_ADDRESS'])
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, data['EMAIL_ADDRESS'], e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, data['EMAIL_ADDRESS'], e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, data['EMAIL_ADDRESS'], e)
			return False


	def insert_organization(self, data):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec insert
			sql = 'insert into T_ORGANIZATIONS_SYNC '\
					'(CN, COMPANY_CD, ORGANIZATION_CD, UPDATE_DATE, SYNC_RESULT, SYNC_TIME, SYNC_FAIL_REASON) '\
					'values (%s, %s, %s, %s, %s, %s, %s)'
			self.cursor.execute(sql,\
					[\
						data['CN'],\
						data['COMPANY_CD'],\
						data['ORGANIZATION_CD'],\
						data['UPDATE_DATE'],\
						data['SYNC_RESULT'],\
						data['SYNC_TIME'],\
						data['SYNC_FAIL_REASON']\
					]\
				)
			logger.info(self.log['230000'], func_name, data['CN'])
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, data['CN'], e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, data['CN'], e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, data['CN'], e)
			return False


	def update_employee(self, data):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec update
			sql = 'update T_EMPLOYEES_SYNC '\
							'set '\
								'DATA_UPD_TIME = %s, '\
								'SYNC_RESULT = %s, '\
								'SYNC_TIME = %s, '\
								'SYNC_FAIL_REASON = %s '\
						'where EMAIL_ADDRESS = %s'
			self.cursor.execute(sql,\
					[\
						data['DATA_UPD_TIME'],\
						data['SYNC_RESULT'],\
						data['SYNC_TIME'],
						data['SYNC_FAIL_REASON'],\
						data['EMAIL_ADDRESS']\
					]\
				)
			logger.info(self.log['230000'], func_name, data['EMAIL_ADDRESS'])
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, data['EMAIL_ADDRESS'], e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, data['EMAIL_ADDRESS'], e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, data['EMAIL_ADDRESS'], e)
			return False


	def update_organization(self, data):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec update
			sql = 'update T_ORGANIZATIONS_SYNC '\
					'set UPDATE_DATE = %s, SYNC_RESULT = %s, SYNC_TIME = %s, SYNC_FAIL_REASON = %s '\
					'where CN = %s'
			self.cursor.execute(sql,\
					[\
						data['UPDATE_DATE'],\
						data['SYNC_RESULT'],\
						data['SYNC_TIME'],\
						data['SYNC_FAIL_REASON'],\
						data['CN']\
					]\
				)
			logger.info(self.log['230000'], func_name, data['CN'])
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, data['CN'], e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, data['CN'], e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, data['CN'], e)
			return False


	def delete_employee(self, email):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec delete
			sql = 'delete from T_EMPLOYEES_SYNC where EMAIL_ADDRESS = %s'
			self.cursor.execute(sql, [email])
			logger.info(self.log['230000'], func_name, email)
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, email, e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, email, e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, email, e)


	def delete_organization(self, cn):
		func_name = sys._getframe().f_code.co_name
		try:
			# exec delete
			sql = 'delete from T_ORGANIZATIONS_SYNC where CN = %s'
			self.cursor.execute(sql, [cn])
			logger.info(self.log['230000'], func_name, cn)
			return True
		except MySQLdb.DataError as e:
			logger.error(self.log['430000'], func_name, cn, e)
			return False
		except MySQLdb.InternalError as e:
			logger.error(self.log['430001'], func_name, cn, e)
			return False
		except MySQLdb.Error as e:
			logger.error(self.log['430002'], func_name, cn, e)
			return False
