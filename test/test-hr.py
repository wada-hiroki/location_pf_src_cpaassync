#!/usr/bin/env python3
# coding: utf-8
import sys
import os
sys.path.append('../')
import configparser
import datetime
from loguru import logger
import hr

os.environ['HTTP_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'
os.environ['HTTPS_PROXY'] = 'https://proxygate2.nic.nec.co.jp:8080'

os.environ['NLS_LANG'] = 'Japanese_Japan.AL32UTF8'

config = configparser.ConfigParser()
config.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')

hr = hr.Hr(config, log)

nowtime = datetime.datetime.now()

hr.update_employees(nowtime)

hr.update_organizations(nowtime)
