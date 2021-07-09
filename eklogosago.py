#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       eklogosago.py
# Version:    0.5
# Purpose:    
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    04.12.2017
# Updated:    04.12.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Get log_osago, log_osago_detail & store it in oracle
Run from cron daily.
'''
import cx_Oracle
Dsn="SITEADMIN/MAKS2017@//172.20.0.182:1521/makcsite"
conn=cx_Oracle.connect(Dsn)
cursor=conn.cursor()
q="select * from log_osago2017 where cdate like '%2017%'"
q1="SELECT max(ID) m FROM log_osago2017"

cursor.execute(q)
#cursor.arraysize=10
print cursor.arraysize
rows=cursor.fetchall()
print cursor.rowcount
#for row in rows:
#	print row
cursor.close()	
conn.close()

