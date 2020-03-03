#!/usr/bin/env python3
# coding: utf-8
import cx_Oracle
import json
import sys
from loguru import logger

class Viewtable():
	def __init__(self, config, log):
		# set config
		self.host = config['viewtable']['host']
		self.port = config['viewtable']['port']
		self.sid = config['viewtable']['sid']
		self.id = config['viewtable']['id']
		self.password = config['viewtable']['password']

		# set logger
		self.log = json.loads(log['viewtable']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)


	def connect_db(self):
		func_name = sys._getframe().f_code.co_name
		try:
			self.tns = cx_Oracle.makedsn(
					self.host,\
					self.port,\
					self.sid\
				)
			self.connection = cx_Oracle.connect(\
					self.id,\
					self.password,\
					self.tns\
				)
			self.cursor = self.connection.cursor()
			return True
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def close_db(self):
		self.connection.close()


	def select_delete_employees(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select * "\
				"from XXX_V_RMT02_KLOUDSPOT "\
				"where DATA_DEL_DATE <= '%s'"\
				% nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_regist_employees(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select K.*, S.JINJICOM_CD "\
						"from XXX_V_RMT02_KLOUDSPOT K "\
							"join XXX_V_SMT02_SOSHIKI S "\
								"on K.SOSHIKI_CD = S.SOSHIKI_CD "\
						"where DATA_UPD_DATE <= '%s'"\
						% nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_update_employees(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select * from XXX_V_RMT02_KLOUDSPOT where DATA_UPD_DATE <= '%s'" % nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_delete_organizations(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select * from XXX_V_SMT02_SOSHIKI where ABOLITION_DATE <= '%s'" % nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_regist_organizations(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select * from XXX_V_SMT02_SOSHIKI where NEW_DATE <= '%s'" % nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_update_organizations(self, nowtime):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select * from XXX_V_SMT02_SOSHIKI where UPDATE_DATE <= '%s'" % nowtime
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False


	def select_organization_name_by_cd(self, cd):
		func_name = sys._getframe().f_code.co_name
		try:
			sql = "select SOSHIKI_NM from XXX_V_SMT02_SOSHIKI where SOSHIKI_CD = '%s'" % cd
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			logger.info(self.log['220000'], func_name, len(rows))
			return rows
		except cx_Oracle.DataError as e:
			logger.error(self.log['420000'], func_name, e)
			return False
		except cx_Oracle.InternalError as e:
			logger.error(self.log['420001'], func_name, e)
			return False
		except cx_Oracle.Error as e:
			logger.error(self.log['420002'], func_name, e)
			return False
