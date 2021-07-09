#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       eklogosgmv.py
# Version:    1.4.3
# Purpose:    Move log-osago* to archive DB server
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    20.06.2018
# Updated:    14.04.2020
# Copyright:  (c) 2018 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Copy b2b.log-osago-* to archive db server and delete source data
'''
import MySQLdb
import sys, os
import datetime


dbParam={
          'ServerSrc':'172.20.0.20',
          'ServerDst':'172.20.22.10',
          'DataBase':'b2b',
          'Table':'',
          'DtField':'cdate',
          'User':'sadmin',
          'Passwd':'trep@let_dba',
          'ExpDate':'0000-00-00'
		 }
tbl=["log_osago", "log_osago_detail", "log_product"]
dtFiewl=["cdate", "datetime", "cdate"]
     
#----------------------------------------------------------------------------
def ekGetTblData(dbparams):
	rows={}
	print "Select data..."
	try:
		dbh=MySQLdb.Connect(host=dbparams['ServerSrc'], user=dbparams['User'], passwd=dbparams['Passwd'],db=dbparams['DataBase'])
		cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from {0} where {1}<'{2}' order by id".format(dbparams['Table'], dbparams['DtField'], dbparams['ExpDate'])
		#sql="select * from {0} order by id".format(dbparams['Table'])
		cur.execute(sql)
		rows=cur.fetchallDict()
	except MySQLdb.DatabaseError, tplDetailError:
		print "ERROR:", tplDetailError.args
		return 0
	print sql
	print "Количество строк=%s" % cur.rowcount
	dbh.close()
	return rows

#----------------------------------------------------------------------------
def ekDictParse(dataset):
	import re
	retval=""
	for k, v in dataset.items():
		if k=='action' or k=='value' or k=='error' or k=='user_agent':
			if not v:
				pass # Write NULL to Mysql
			else:
				retval=retval+"{0}='{1}',".format(k,re.escape(v))
		else:
			retval=retval+"{0}='{1}',".format(k,v)
	return retval[:-1]
#----------------------------------------------------------------------------
def ekSendTblData(dbparams, dataset):
	i=0
	tblName="{0}_{1}".format(dbparams['Table'], dbparams['ExpDate'].strftime("%Y"))
	print "Transfer data..."
	try:
		dbh=MySQLdb.Connect(host=dbparams['ServerDst'], user=dbparams['User'], passwd=dbparams['Passwd'],db=dbparams['DataBase'])
		#cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cur=dbh.cursor()
		cur.execute("set names 'utf8'")
		for row in dataset:
			sql="insert into %s set %s" % (tblName, ekDictParse(row))
			try:
				cur.execute(sql)
				#pass
			except MySQLdb.DatabaseError, tplDetailError:
				print "ERROR:", tplDetailError.args, dbparams['ServerDst'], sql
				continue
	except MySQLdb.DatabaseError, tplDetailError:
		print "ERROR:", tplDetailError.args, dbparams['ServerDst']
		return 0
	dbh.close()
	#print "Количество строк=%s" % cur.rowcount
	return 1

#----------------------------------------------------------------------------
def ekDelTblData(dbparams, retval):
	if not retval:
		return 0
		
	print "Delete data..."
	try:
		dbh=MySQLdb.Connect(host=dbparams['ServerSrc'], user=dbparams['User'], passwd=dbparams['Passwd'],db=dbparams['DataBase'])
		cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="delete from {0} where {1}<'{2}'".format(dbparams['Table'], dbparams['DtField'], dbparams['ExpDate'])
		cur.execute(sql)
		sql="optimize table {0}".format(dbparams['Table'])
		cur.execute(sql)
	except MySQLdb.DatabaseError, tplDetailError:
		print "ERROR:", tplDetailError.args
		return 0
	dbh.close()
	return 1

#----------------------------------------------------------------------------
def showtbldata(dataset):
	for row in dataset:
		for k,v in row.items():
			print "{0} = {1}".format(k,v)
		print "------------------"

#----------------------------------------------------------------------------
def main():
	reval={}
	i=0
	workDate=datetime.date.today()
	dbParam['ExpDate']=workDate-datetime.timedelta(4)
	print "-----{0}-----".format(workDate)
	#print "-----{0}-----".format(dbParam['ExpDate'])
	print "Start files transfer..."
	#for i in xrange(len(tbl)):
	for i in xrange(3):
		dbParam['Table']=tbl[i]
		dbParam['DtField']=dtFiewl[i]
		print "Table = {0}".format(dbParam['Table'])
		retval=ekGetTblData(dbParam)
		if not retval:
			print retval
			continue
		#showtbldata(retval)
		retval=ekSendTblData(dbParam, retval)
		#retval=0
		ekDelTblData(dbParam, retval)
			
	return 0

if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
#
