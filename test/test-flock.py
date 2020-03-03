#!/usr/bin/env python3
# coding: utf-8
import sys
import time
sys.path.append('../')

import flock
import configparser

conf = configparser.ConfigParser()
conf.read('../conf/config.ini', encoding='utf-8')

log = configparser.ConfigParser()
log.read('../conf/log.ini', encoding='utf-8')

flock_obj = flock.Flock(conf, log)
if not flock_obj.lock():
	sys.exit()
time.sleep(5)
# Unlock
#flock_obj.unlock()
