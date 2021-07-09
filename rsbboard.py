#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       rsbboard.py
# Version:    1.0.0
# Purpose:    Delete expired records in RSBBoard table.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    12.12.2007
# Updated:   12.12.2007
# Copyright:  (c) 2007 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Delete expired records in RSBBoard table
Run from cron.
'''
import sys, os
import MySQLdb
from time import localtime, strftime

dbParam={'Server':'dbserver', 'DBName':'rsbcommon', 'Table':'RSBBoard', 'User':'webuser', 'Passwd':'Dt,>pth', 'Dbh':'', 'Record':''}

#---------------------------------------------------------------------------
def ekDelExpRec(dbParam):
  retVal=[]
  #sSql="delete from `%s` where  now() > date_add(`cDate`, INTERVAL `iExpire` day)" % dbParam['Table']
  sSql="delete from `%s` where ID='%d'" % (dbParam['Table'], dbParam['Record'])
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #print "Строка запроса: %s" % sSql
    cur.execute(sSql)
    res=cur.fetchone()
    dbh.close()
  except MySQLdb.DatabaseError, tDetailError:
    print "ERROR: ", tDetailError.args
  return 0
#---------------------------------------------------------------------------
def ekGetExpRec(dbParam):
  retVal=[]
  sSql="select * from `%s` where  now() > date_add(`cDate`, INTERVAL `iExpire` day)" % dbParam['Table']
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #print "Строка запроса: %s" % sSql
    cur.execute(sSql)
    res=cur.fetchall()
    for row in res:
      print "Delete record: ID=%s Date=%s Expire Days=%s" % (row['ID'], row['cDate'], row['iExpire'])
      dbParam['Record']=row['ID']
      ekDelExpRec(dbParam)
    dbh.close()
  except MySQLdb.DatabaseError, tDetailError:
    print "ERROR: ", tDetailError.args
  return 0
#---------------------------------------------------------------------------
def main():
  print "-----",strftime("%d.%m.%Y", localtime()),"-----"
  ekGetExpRec(dbParam)
  return 0
  
if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
