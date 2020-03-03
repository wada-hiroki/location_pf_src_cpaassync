#!/usr/bin/env python3
# coding: utf-8
import sys
import json
from loguru import logger

import viewtable
import cooperation
import employee
import organization


class Hr():
	def __init__(self, config, log):
		# Create object
		self.view = viewtable.Viewtable(config, log)
		self.coop = cooperation.Cooperation(config, log)
		self.employee = employee.Employee(config, log)
		self.organization = organization.Organization(config, log)

		# set logger
		self.log = json.loads(log['hr']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)


	def update_employees(self, nowtime):
		# Set function name
		func_name = sys._getframe().f_code.co_name

		# Connect to database of view
		if not self.view.connect_db():
			print()
			return False

		# Connect to database of cooperation
		if not self.coop.connect_db():
			return False

		# Set ignore list
		delete_list = []
		regist_list = []

		#### Delete employees from Location Platform
		# Get delete employees list
		delete_list = self.view.select_delete_employees(nowtime)
		if len(delete_list) > 0:
			for employee in delete_list:
				if not isinstance(employee, tuple) or not len(employee) == 19:
					logger.warning(self.log['370000'], func_name, employee)
					continue
				# Set view data
				email = employee[0]
				# Delete employee
				self.employee.delete(employee, nowtime)
				# Append employee to delete_list if delete it from Location Platform.
				# And if faild delete employee is same.
				delete_list.append(email)

		#### Regist employees to Location Platform
		# Get post employees list
		regist_list = self.view.select_regist_employees(nowtime)
		if len(regist_list) > 0:
			for employee in regist_list:
				if not isinstance(employee, tuple) or not len(employee) == 19:
					logger.warning(self.log['370000'], func_name, employee)
					continue
				# Set view data
				email = employee[0]
				# Skip regist employee if exists it in delete_list
				if email in delete_list:
					continue
				# Skip regist employee if exists it in T_EMPLOYEES_SYNC
				if len(self.coop.select_employee(email)) > 0:
					continue
				# Regist employee
				self.employee.regist(employee, nowtime)
				# Append employee to regist_list if regist it from Location Platform.
				# And if faild regist employee is same.
				regist_list.append(email)

		#### Update employees to Location Platform
		# Get update employees list
		update_list = self.view.select_update_employees(nowtime)
		if len(update_list) > 0:
			for employee in update_list:
				if not isinstance(employee, tuple) or not len(employee) == 19:
					logger.warning(self.log['370000'], func_name, employee)
					continue
				# Set view data
				email = employee[0]
				# Skip update employee if exists it in delete_list or regist_list
				if email in delete_list or email in regist_list:
					continue
				# Update employee
				self.employee.update(employee, nowtime)

		# Close from database for viewtable
		self.view.close_db()

		# Close from database of cooperation
		self.coop.close_db()

		return True


	def update_organizations(self, nowtime):
		# Set function name
		func_name = sys._getframe().f_code.co_name

		# Connect to database of view
		if not self.view.connect_db():
			return False

		# Connect to database of cooperation
		if not self.coop.connect_db():
			return False

		# Set ignore list
		delete_list = []
		regist_list = []

		#### Delete organizations from Location Platform
		# Get delete organizations list
		delete_list = self.view.select_delete_organizations(nowtime)
		if len(delete_list) > 0:
			for organization in delete_list:
				if not isinstance(organization, tuple) or not len(organization) == 20:
					logger.warning(self.log['370000'], func_name, organization)
					continue
				# Set view data
				unique_cd = organization[14]
				# Delete organization
				self.organization.delete(organization, nowtime)
				# Append organization to delete_list if delete it from Location Platform.
				# And if faild delete organization is same.
				delete_list.append(unique_cd)

		#### Regist organizations to Location Platform
		# Get post organizations list
		regist_list = self.view.select_regist_organizations(nowtime)
		if len(regist_list) > 0:
			for organization in regist_list:
				if not isinstance(organization, tuple) or not len(organization) == 20:
					logger.warning(self.log['370000'], func_name, organization)
					continue
				# Set view data
				unique_cd = organization[14]
				# Skip regist organzaif exists it in delete_list
				if unique_cd in delete_list:
					continue
				# Skip regist organization if exists it in T_EMPLOYEES_SYNC
				if len(self.coop.select_organization(unique_cd)) > 0:
					continue
				# Regist organization
				self.organization.regist(organization, nowtime)
				# Append organization to regist_list if regist it from Location Platform.
				# And if faild regist organization is same.
				regist_list.append(unique_cd)

		#### Update organizations to Location Platform
		# Get update organizations list
		update_list = self.view.select_update_organizations(nowtime)
		if len(update_list) > 0:
			for organization in update_list:
				if not isinstance(organization, tuple) or not len(organization) == 20:
					logger.warning(self.log['370000'], func_name, organization)
					continue
				# Set view data
				unique_cd = organization[14]
				# Skip update organization if exists it in delete_list or regist_list
				if unique_cd in delete_list or unique_cd in regist_list:
					continue
				# Update organization
				self.organization.update(organization, nowtime)

		# Close from database for viewtable
		self.view.close_db()

		# Close from database of cooperation
		self.coop.close_db()

		return True
