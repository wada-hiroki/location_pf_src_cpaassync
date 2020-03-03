#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append('../')
import configparser
import datetime
import employee
import cooperation
import os
from loguru import logger

os.environ['HTTP_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
os.environ['HTTPS_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'

config = configparser.ConfigParser()
config.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')


nowtime = datetime.datetime.now()

coop = cooperation.Cooperation(config, log)
emp = employee.Employee(config, log)

regist = [\
		'wada.hiroki@nesic.com',\
		'和田',\
		'大樹',\
		'わだ',\
		'ひろき',\
		'Wada',\
		'Hiroki',\
		'ビジネス統括本部ＤＸ',\
		'50-15-25-10',\
		'ワダ',\
		'ヒロキ',\
		'役職名',\
		'JOB_CLASS_CD',\
		'LEVEL_CD',\
		'PARTNER_KBN',\
		'KOJIN_SYOKUSEI_CD',\
		'2020-01-31 06:00:00.123456',\
		'',\
		''\
	]

update = [\
		'wada.hiroki@nesic.com',\
		'和田-edit',\
		'大樹-edit',\
		'わだ-edit',\
		'ひろき-edit',\
		'Wada-edit',\
		'Hirok-editi',\
		'テスト株式会社技術部-edit',\
		'1-1-1-edit',\
		'ワダ-edit',\
		'ヒロキ-edit',\
		'役職名-edit',\
		'JOB_CLASS_CD',\
		'LEVEL_CD',\
		'PARTNER_KBN',\
		'KOJIN_SYOKUSEI_CD',\
		'2020-01-31 06:00:00.123456',\
		'2020-02-17 06:00:00.123456',\
		''\
	]

delete = [\
		'wada.hiroki@nesic.com',\
		'和田-edit',\
		'大樹-edit',\
		'わだ-edit',\
		'ひろき-edit',\
		'Wada-edit',\
		'Hirok-editi',\
		'テスト株式会社技術部-edit',\
		'1-1-1-edit',\
		'ワダ-edit',\
		'ヒロキ-edit',\
		'役職名-edit',\
		'JOB_CLASS_CD',\
		'LEVEL_CD',\
		'PARTNER_KBN',\
		'KOJIN_SYOKUSEI_CD',\
		'2020-01-31 06:00:00.123456',\
		'2020-02-17 06:00:00.123456',\
		'2020-02-18 06:00:00.123456'
	]

coop.connect_db()

print('-- Regist Employee to Location Platform --')
print('-- Result')
if emp.regist(regist, nowtime):
	print('OK')
else:
	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_EMPLOYEES_SYNC')
print(coop.select_employee(regist[0]))

print('-- Update Employee to Location Platform --')
print('-- Result')
if emp.update(update, nowtime):
	print('OK')
else:
	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_EMPLOYEES_SYNC')
print(coop.select_employee(update[0]))

print('-- Delete Employee from Location Platform --')
print('-- Result')
#if emp.delete(delete, nowtime):
#	print('OK')
#else:
#	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_EMPLOYEES_SYNC')
print(coop.select_employee(delete[0]))

coop.close_db()
