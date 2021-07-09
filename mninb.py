#!/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       mninb.py
# Version:    1.0.7
# Purpose:    Mail notify about update table in InetBank database
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    30.11.2005
# Updated:    05.05.2006
# Copyright:  (c) 2005 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Mail notification about update table in InetBank database.
Run from cron.
'''
import getopt, os, sys, smtplib
from time import localtime, strftime
from datetime import time, timedelta
import MySQLdb

dbParam={'Server':'dbserver', 'DBName':'InetBank', 'Table':'CLIENTS_TIME', 'User':'InetBankUser', 'Passwd':'ghbrjk2000'}
workTime=(11, 21)
maxDelay=70
smtpServer="10.0.1.17"
addrFrom="webadmin@russlavbank.com"
addrTo=("barry@russlavbank.com", "repaa@russlavbank.com", "avh@russlavbank.com", "stikin@russlavbank.com", "fyodor@russlavbank.com", "julia@russlavbank.com")
addrErrorTo=("barry@russlavbank.com", "repaa@russlavbank.com")
#---------------------------------------------------------------------------
def ekGetINBLastUpTime(dbParam):
  retVal={'Error':"", 'Minutes':0, 'Hours':0}
  sSql="select THE_TIME from %s" % (dbParam["Table"])
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
#    print "Строка запроса: " % sSql
    cur.execute(sSql)
    res=cur.fetchone()
    retVal['Hours']=res['THE_TIME'][0:2]
    retVal['Minutes']=res['THE_TIME'][2:]
    print retVal
    dbh.close()
  except MySQLdb.DatabaseError, tplDetailError:
#      print "ERROR:", tplDetailError.args
      retVal['Error']=tplDetailError.args
  return retVal
#---------------------------------------------------------------------------
def ekSendmail(mailServer, mailFrom, mailTo, msg):
  mailMsg = ""
  try:
    smtpServer=smtplib.SMTP(host=mailServer)
    for mailToItem in mailTo:
      print "Send mail to: ", mailToItem
      mailMsg = """Subject: InetBank notification. Error! \nFrom: %s\nTo: %s\nMIME-Version: 1.0\nContent-Type: text/plain;charset="Windows-1251"\n\n%s""" % (mailFrom, mailToItem, msg)
      #print mailMsg.encode("cp1251")
      smtpServer.sendmail(mailFrom, mailToItem, mailMsg)
    smtpServer.quit()
  except smtplib.SMTPException:
    print "ERROR:", tplDetailError.args
    
#---------------------------------------------------------------------------
def main():
  dRetVal=ekGetINBLastUpTime(dbParam)
  clt=localtime()
  tmCurrent=timedelta(minutes=clt[4], hours=clt[3])
  tmStored=timedelta(minutes=int(dRetVal['Minutes']), hours=int(dRetVal['Hours']))
  tmDelay=(tmCurrent-tmStored).seconds/60
  msg="InetBank.\n\nUpdate delay: %s min.\n\nTime in InetBank table: %s\nCurrent time: %s """ % (tmDelay, tmStored, tmCurrent)
  msgError="InetBank.\n\nError time: %s\nMySql Error: %s" % (strftime("%d.%m.%Y %H:%M:%S",clt), dRetVal['Error'])
  try:
    if(dRetVal['Error']!=""):
      ekSendmail(smtpServer, addrFrom, addrErrorTo, msgError)
      print dRetVal['Error']
   #
   #clt[6] - day of week. Do not work on weekend. clt[6]=0 - Monday
   #
    elif(clt[6]<5 and clt[3]>=workTime[0] and clt[3]<workTime[1]):
      if(tmDelay>maxDelay):
        ekSendmail(smtpServer, addrFrom, addrTo, msg)
  finally:
    #ekSendmail(smtpServer, addrFrom, addrTo, msg)
    print "\nDone ;)\n------------------------------"
  return 0

if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
