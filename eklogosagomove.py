#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
import MySQLdb
dbServer="172.20.0.20"
dbName="b2b"
tblName="log_osago"
dbUser="figaro"
dbPasswd="Abufh0nfv"
dbParam={'Server':'172.20.0.20',
          'DataBase':'b2b',
          'Table':'log_osago',
          'User':'figaro',
          'Passwd':'Abufh0nfv'
		 }
dbh=MySQLdb.Connect(host=dbParam['Server'], user=dbParam['User'], passwd=dbParam['Passwd'],db=dbParam['DataBase'])
cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
sSql="select * from log_osago limit 0,10"
cur.execute(sSql)
for row in cur.fetchallDict():
	print row['id'], row['programm'], row['action'], row['ip'], row['user_agent'], row['session_id'], row['cdate'], row['file'], row['line']
