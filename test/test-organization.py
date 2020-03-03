#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append('../')
import configparser
import datetime
import os
import time
import organization
import cooperation
from loguru import logger

os.environ['HTTP_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
os.environ['HTTPS_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'


config = configparser.ConfigParser()
config.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')


nowtime = datetime.datetime.now()

coop = cooperation.Cooperation(config, log)
org = organization.Organization(config, log)

regist = [\
		'113305',\
		'NECネッツエスアイ株式会社',\
		'NEC Networks & System Integration Corporation',\
		'NESIC',\
		'NESIC_RYAKU',\
		'2020-01-31 06:00:00.123456',\
		'',\
		'10-20-30-40',\
		'1010',\
		'和田テスト組織',\
		'和田略組織',\
		'10',\
		'10',\
		'UP_SOHIKI_CD',\
		'UNIQUE_CD',\
		'',\
		'20',\
		'2',\
		'33',\
		'123456'\
	]

update = [\
		'113305',\
		'NECネッツエスアイ株式会社',\
		'NEC Networks & System Integration Corporation',\
		'NESIC',\
		'NESIC_RYAKU',\
		'2020-01-31 06:00:00.123456',\
		'2020-02-02 06:00:00.123456',\
		'10-20-30-40',\
		'1010',\
		'和田テスト組織',\
		'和田略組織',\
		'10',\
		'10',\
		'UP_SOHIKI_CD',\
		'UNIQUE_CD',\
		'2020-02-01 12:00:00.123456',\
		'20',\
		'2',\
		'33',\
		'123456'\
	]

delete = [\
		'113305',\
		'NECネッツエスアイ株式会社',\
		'NEC Networks & System Integration Corporation',\
		'NESIC',\
		'NESIC_RYAKU',\
		'2020-01-31 06:00:00.123456',\
		'2020-02-03 06:00:00.123456',\
		'10-20-30-40',\
		'1010',\
		'和田テスト組織',\
		'和田略組織',\
		'10',\
		'10',\
		'UP_SOHIKI_CD',\
		'UNIQUE_CD',\
		'2020-02-01 12:00:00.123456',\
		'20',\
		'2',\
		'33',\
		'123456'\
	]

coop.connect_db()

print('-- Regist Organization to Location Platform --')
print('-- Result')
if org.regist(regist, nowtime):
	print('OK')
else:
	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_ORGANIZATIONS_SYNC')
print(coop.select_organization(regist[14]))

coop.close_db()
coop.connect_db()

print('-- Update Organization to Location Platform --')
print('-- Result')
if org.update(update, nowtime):
	print('OK')
else:
	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_ORGANIZATIONS_SYNC')
print(coop.select_organization(update[14]))

coop.close_db()
coop.connect_db()

print('-- Delete Organization from Location Platform --')
print('-- Result')
if org.delete(delete, nowtime):
	print('OK')
else:
	print('NG')
print('-- Now Time')
print(str(datetime.datetime.now()))
print('-- T_ORGANIZATIONS_SYNC')
print(coop.select_organization(delete[14]))

coop.close_db()
