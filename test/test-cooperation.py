#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append('../')

import configparser
import cooperation
from loguru import logger

conf = configparser.ConfigParser()
conf.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')

coop = cooperation.Cooperation(conf, log)

coop.connect_db()

emp_body = {\
		'EMAIL_ADDRESS': 'wada.hiroki@nesic.com',\
		'DATA_UPD_TIME': '2020-01-26 19:36:22.344323',\
		'SYNC_TIME': '2020-01-26 19:36:22.344323',\
		'SYNC_RESULT': 0,\
		'SYNC_FAIL_REASON': ''\
	}

coop.insert_employee(emp_body)
coop.commit_db()
print('-- Employee Insert Result --')
print(coop.select_employee(emp_body['EMAIL_ADDRESS']))
print(emp_body['EMAIL_ADDRESS'])

emp_body['SYNC_RESULT'] = 1
emp_body['SYNC_FAIL_REASON'] = 'Database Error'
coop.update_employee(emp_body)
coop.commit_db()
print('-- Employee Update Result --')
print(coop.select_employee(emp_body['EMAIL_ADDRESS']))

coop.delete_employee(emp_body['EMAIL_ADDRESS'])
coop.commit_db()
print('-- Employee Delete Result --')
print(coop.select_employee(emp_body['EMAIL_ADDRESS']))

org_body = {\
		'CN': '1133051151488',\
		'COMPANY_CD': '113305',\
		'ORGANIZATION_CD': '1-1-1',\
		'UPDATE_DATE': '2020-01-26 19:36:22.344323',\
		'SYNC_TIME': '2020-01-26 19:36:22.344323',\
		'SYNC_RESULT': 0,\
		'SYNC_FAIL_REASON': ''\
	}

coop.insert_organization(org_body)
coop.commit_db()
print('-- Organization Insert Result --')
print(coop.select_organization(org_body['CN']))

org_body['SYNC_RESULT'] = 1
org_body['SYNC_FAIL_REASON'] = 'Database Error'
coop.update_organization(org_body)
coop.commit_db()
print('-- Organization Update Result --')
print(coop.select_organization(org_body['CN']))

coop.delete_organization(org_body['CN'])
coop.commit_db()
print('-- Organization Delete Result --')
print(coop.select_organization(org_body['CN']))

print('-- Rollback test --')
coop.insert_organization(org_body)
coop.insert_organization(org_body)

coop.close_db()
