#!/usr/bin/env python3
# coding: utf-8
import urllib.request
import json
import re
import sys
from loguru import logger

class LocationPf():
	def __init__(self, config, log):
		# get config
		self.res_pattern = config['locationpf']['res_pattern']
		self.contenttype = config['locationpf']['contenttype']
		self.authorization = config['locationpf']['authorization']
		self.employees_api = config['locationpf']['url'] + config['locationpf']['employees']
		self.organizations_api = config['locationpf']['url'] + config['locationpf']['organizations']

		# set logger
		self.log = json.loads(log['locationpf']['log'])
		logfile = config['logger']['logfile']
		rotation = config['logger']['rotation']
		retention = int(config['logger']['retention'])
		logger.remove()
		logger.add(logfile, rotation=rotation, retention=retention)

		# set request parameter required list
		self.param_require = {\
				'patch_employee': config['locationpf']['patch_emp_param_require'],\
				'patch_organization': config['locationpf']['patch_org_param_require'],\
				'delete_employee': config['locationpf']['delete_emp_param_require'],\
				'delete_organization': config['locationpf']['delete_org_param_require']\
			}
		# set request parameter regular expression
		self.param_regex = {\
				'patch_employee': config['locationpf']['patch_emp_param_regex'],\
				'patch_organization': config['locationpf']['patch_org_param_regex']\
			}

		# set request body required list
		self.body_require = {\
				'post_employee': config['locationpf']['post_emp_body_require'],\
				'post_organization': config['locationpf']['post_org_body_require'],\
				'patch_employee': config['locationpf']['patch_emp_body_require'],\
				'patch_organization': config['locationpf']['patch_org_body_require']\
			}
		# set request body regular expression
		self.body_regex = {\
				'post_employee': config['locationpf']['post_emp_body_regex'],\
				'post_organization': config['locationpf']['post_org_body_regex'],\
				'patch_employee': config['locationpf']['patch_emp_body_regex'],\
				'patch_organization': config['locationpf']['patch_org_body_regex']\
			}


	def validate_request_body(self, params, func_name):
		for param in self.body_regex:
			# check require body parameter
			if param in self.body_require[func_name] and params[param] is None:
				logger.error(self.log['410001'], func_name, param)
				return False

			# check body parameter format
			pattern = re.compile(self.body_regex[param])
			if pattern.match(params[param]) is None:
				logger.error(sefl.log['410002'], func_name, param)
				return False


	def validate_request_param(self, params, func_name):
		for param in self.param_regex:
			# check require uri parameter
			if param in self.param_require[func_name] and params[param] is None:
				logger.error(self.log['410003'], func_name, param)
				return False

			# check uri parameter format
			pattern = re.compile(self.body_regex[param])
			if pattern.match(params[param]) is None:
				logger.error(sefl.log['410004'], func_name, param)
				return False


	def post_employee(self, json_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request body
		#if self.validate_request_body(json_params, func_name):
		#	return False

		# prepair http request contents
		method = "POST"
		headers = {\
				'Content-type':'application/json',\
				'Authorization':self.authorization\
			}
		json_data = json.dumps(json_params).encode("utf-8")

		# exec http request
		req = urllib.request.Request(\
				self.employees_api,\
				data = json_data,\
				headers = headers,\
				method = method\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210000'], func_name, json_params['emailAddress'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410005'], func_name, json_params['emailAddress'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410006'], func_name, json_params['emailAddress'], e)
			return False


	def post_organization(self, json_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request body
		#if self.validate_request_body(json_params, func_name):
		#	return False

		# prepair http request contents
		method = "POST"
		headers = {\
				'Content-type':'application/json',\
				'Authorization':self.authorization\
			}
		json_data = json.dumps(json_params).encode("utf-8")

		# exec http request
		req = urllib.request.Request(\
				self.organizations_api,\
				data = json_data,\
				headers = headers,\
				method = method\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210001'], func_name, json_params['companyCd'], json_params['organizationCd'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410007'], func_name, json_params['companyCd'], json_params['organizationCd'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410008'], func_name, json_params['companyCd'], json_params['organizationCd'], e)
			return False


	def patch_employee(self, uri_params, json_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request param
		#if self.validate_request_param(uri_params, func_name):
		#	return False
		# validate request body
		#if self.validate_request_body(json_params, func_name):
		#	return False

		# create url
		url = self.employees_api + '?' + urllib.parse.urlencode(uri_params)

		# prepair http request contents
		method = "PATCH"
		headers = {\
				'Content-type':'application/json',\
				'Authorization':self.authorization\
			}
		json_data = json.dumps(json_params).encode("utf-8")

		# exec http request
		req = urllib.request.Request(\
				url,\
				data = json_data,\
				headers = headers,\
				method = method,\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210000'], func_name, uri_params['emailAddress'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410005'], func_name, uri_params['emailAddress'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410006'], func_name, uri_params['emailAddress'], e)
			return False


	def patch_organization(self, uri_params, json_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request param
		#if self.validate_request_param(uri_params, func_name):
		#	return False
		# validate request body
		#if self.validate_request_body(json_params, func_name):
		#	return False

		# create url
		url = self.organizations_api + '?' + urllib.parse.urlencode(uri_params)

		# prepair http request contents
		method = "PATCH"
		headers = {\
				'Content-type':'application/json',\
				'Authorization':self.authorization\
			}
		json_data = json.dumps(json_params).encode("utf-8")

		# exec http request
		req = urllib.request.Request(\
				url,\
				json_data,\
				headers,\
				method = method,\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210001'], func_name, uri_params['companyCd'], uri_params['organizationCd'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410007'], func_name, uri_params['companyCd'], uri_params['organizationCd'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410008'], func_name, uri_params['companyCd'], uri_params['organizationCd'], e)
			return False


	def delete_employee(self, uri_params, json_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request param
		#if self.validate_request_param(uri_params, func_name):
		#	return False

		# create url
		url = self.employees_api + '?' + urllib.parse.urlencode(uri_params)

		# prepair http request contents
		method = "DELETE"
		headers = {\
				'Content-type':'application/json',\
				'Authorization': self.authorization\
			}
		json_data = json.dumps(json_params).encode("utf-8")

		# exec http request
		req = urllib.request.Request(\
				url,\
				data = json_data,\
				headers = headers,\
				method = method\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210000'], func_name, uri_params['emailAddress'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410005'], func_name, uri_params['emailAddress'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410006'], func_name, uri_params['emailAddress'], e)
			return False


	def delete_organization(self, uri_params):
		# get my function name
		func_name = sys._getframe().f_code.co_name
		# validate request param
		#if self.validate_request_param(uri_params, func_name):
		#	return False

		# create url
		url = self.organizations_api + '?' + urllib.parse.urlencode(uri_params)

		# prepair http request contents
		method = "DELETE"
		headers = {\
				'Content-type':'application/json',\
				'Authorization':self.authorization\
			}

		# exec http request
		req = urllib.request.Request(\
				url,\
				headers = headers,\
				method = method\
			)
		try:
			with urllib.request.urlopen(req) as res:
				res_code = res.getcode()
				logger.info(self.log['210001'], func_name, uri_params['companyCd'], uri_params['organizationCd'])
				return True
		except urllib.error.HTTPError as e:
			logger.error(self.log['410007'], func_name, uri_params['companyCd'], uri_params['organizationCd'], e)
			return False
		except urllib.error.URLError as e:
			logger.error(self.log['410008'], func_name, uri_params['companyCd'], uri_params['organizationCd'], e)
			return False
