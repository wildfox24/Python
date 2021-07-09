#!/usr/bin/env python
# -*- coding: utf8 -*-
#----------------------------------------------------------------------------
# Name:       sflor.py
# Version:    1.0.0
# Purpose:    Send file to list of recipients. List is stored in DB.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    26.11.2007
# Updated:    26.11.2007
# Copyright:  (c) 2007 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Send file to recipients by mail list stored in DB.
Run from cron.
'''
import sys, os, glob
import MySQLdb
from time import localtime, strftime

sPath="/home/klek/temp/balances/"
dbParam={'Server':'dbserver', 'DBName':'rsbcommon', 'Table':'RSBMailList', 'User':'webuser', 'Passwd':'Dt,>pth'}
smtpServer="10.0.1.17"

#---------------------------------------------------------------------------
def ekGetListOfRecipients(dbParam):
  retVal=[]
  sSql="select * from %s" % (dbParam["Table"])
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #print "Строка запроса: " % sSql
    cur.execute(sSql)
    res=cur.fetchall()
    retVal=[row for row in res]
    print retVal
    dbh.close()
  except MySQLdb.DatabaseError, tplDetailError:
    print "ERROR:", tplDetailError.args
  return retVal
#---------------------------------------------------------------------------
def ekGetFileList(sPath):
  lFiles=[]
  #lFiles=os.listdir(sPath)
  lFiles=([os.path.basename(f) for f in glob.glob(sPath+'*.zip')])
  return lFiles
#---------------------------------------------------------------------------
def main():
  sFile=""
  sCurFName=strftime("%Y%m", localtime())
  print "-----",strftime("%d.%m.%Y", localtime()),"-----"
  lFiles=ekGetFileList(sPath)
  lFiles.sort()
  lFiles.reverse()
  print lFiles
  #print sCurFName+".zip"
  try:
    sFile=lFiles[lFiles.index(sCurFName+".zip1")]
  except:
    print "ERROR: File %s no exist..." %  (sCurFName+".zip1",)
    return -1 #No such file
  lRecipients=ekGetListOfRecipients(dbParam)
  for Recipient in lRecipients:
    print Recipient['ID'], Recipient['Email'], Recipient['DT']
  return 0
  
if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
