#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append('../')

import configparser
import viewtable
import datetime
from loguru import logger

conf = configparser.ConfigParser()
conf.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')

view = viewtable.Viewtable(conf, log)

view.connect_db()

nowtime = datetime.datetime.now()
print(nowtime)

print('-- select_delete_employees --')
print(view.select_delete_employees(nowtime))

print('-- select_regist_employees --')
print(view.select_regist_employees(nowtime))

print('-- select_update_employees --')
print(view.select_update_employees(nowtime))

print('-- select_delete_employees --')
print(view.select_delete_organizations(nowtime))

print('-- select_regist_organizations --')
print(view.select_regist_organizations(nowtime))

print('-- select_organization_name_by_cd --')
print(view.select_organization_name_by_cd('65-50-06'))

view.close_db()
