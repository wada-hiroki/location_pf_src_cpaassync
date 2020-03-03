#!/usr/bin/env python3
# coding: UTF-8
import os
import sys
sys.path.append('../')

import configparser
import locationpf
from loguru import logger
import datetime

conf = configparser.ConfigParser()
conf.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')

api = locationpf.LocationPf(conf, log)

nowtime = datetime.datetime.now()

os.environ['HTTP_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
os.environ['HTTPS_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'

post_emp_json = {\
		'emailAddress': 'wada.hiroki@nesic.com',\
		'lastName': 'test',\
		'firstName': 'tarou',\
		'companyCd': '113305',\
		'organizationCd': '1-1-1',\
		'presense': 1,\
		'enabled': 1\
	}

emp_uri = {\
		'emailAddress': 'wada.hiroki@nesic.com'\
	}
patch_emp_json = {\
		'lastName': 'test-patch'\
	}

post_org_json = {\
		"companyCd": "com001",\
		"companyName": "NECネッツアイ株式会社",\
		"organizationCd": "55-30-43-15",\
		"organizationName": "組織名",\
		"organizationShort": "組織名(略称)",\
		"organizationLevel": 1,\
		"organizationLevelCd": "15",\
		"organizationParentCd": "55-30-43",\
		"organizationSort": 1\
	}

org_uri = {\
		'companyCd': 'com001',\
		'organizationCd': '55-30-43-15'\
	}

patch_org_json = {\
		"companyName": "NECネッツアイ株式会社-edit",\
		"organizationName": "組織名-edit",\
		"organizationShort": "組織名(略称)-edit",\
		"organizationLevel": 1,\
		"organizationLevelCd": "15",\
		"organizationParentCd": "55-30-43",\
		"organizationSort": 1\
	}

print('-- Post Employees --')
if api.post_employee(post_emp_json):
	print('result: OK')
else:
	print('result: NG')
print('-- Patch Employees --')
if api.patch_employee(emp_uri, patch_emp_json):
	print('result: OK')
else:
	print('result: NG')
print('-- Delete Employees --')
if api.delete_employee(emp_uri, emp_uri):
	print('result: OK')
else:
	print('result: NG')

print('-- Post Organizations --')
if api.post_organization(post_org_json):
	print('result: OK')
else:
	print('result: NG')
print('-- Patch Organizations --')
if api.patch_organization(org_uri, patch_org_json):
	print('result: OK')
else:
	print('result: NG')
print('-- Delete Organizations --')
if api.delete_organization(org_uri, org_uri):
	print('result: OK')
else:
	print('result: NG')
