#!/usr/bin/env python
# -*- coding: windows-1251 -*-
#----------------------------------------------------------------------------
import MySQLdb
dbServer="172.20.0.20"
dbName="b2b"
tblName="log_osago"
dbUser="figaro"
dbPasswd="Abufh0nfv"
sSql=""

dbh=MySQLdb.Connect(host=dbServer,user=dbUser,passwd=dbPasswd,db=dbName)
cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cur1=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sSql1="select * from log_osago"
cur.execute(sSql1)
#for row in cur.fetchallDict():
#  sSql="INSERT INTO %s (Date, NumCode, CharCode, Nominal, Name, Value) values('%s', '%d', '%s', '%d', '%s', '%9.4f')" % \
#           (tblName, row['Cur_Date'], row['N_kod'], row['C_kod'], row['Unit'], row['Valuta'], row['Kurs'])
#  print "Строка запроса: '%s'" % sSql
#  cur1.execute(sSql)
dbh.close()
