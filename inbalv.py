#!/bin/env python
# -*- coding: cp1251 -*-
#----------------------------------------------------------------------------
# Name:       ibalv.py
# Version:    1.4
# Purpose:    InetBank Access Log Viewer
#
# Author:     Eugene Klepikov
# E-Mail:     klekfox@mail.ru
#
# Created:    15.07.2004
# Updated:    20.04.2005
# Copyright:  (c) 2004 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Хорошая прога ;)
'''
import sys, getopt
from time import localtime, strftime
import smtplib
import MySQLdb

smtpServer="wwwrsb"
dbServer="dbserver"
dbName="InetBank"
dbUser="webuser"
dbPasswd="Dt,>pth"
tblName="InetBankLog"
#---------------------------------------------------------------------------
def ekSendmail(MailServer, MailFrom, MailTo, MailSubject, MailMsg):
  MailHeader="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (MailFrom, MailTo, MailSubject)
  print "Send mail to: ", MailTo
  try:
    smtpServer=smtplib.SMTP(host=MailServer)
    smtpServer.sendmail(MailFrom, MailTo, MailHeader+MailMsg)
    smtpServer.quit()
  except:
    print "ERROR: send mail failure"
    
#---------------------------------------------------------------------------
def main():
  sSql=""
  sAddrFrom="webadmin@russlavbank.com"
  #tAddrTo=("barry@russlavbank.com", "welcome@russlavbank.com", "webmaster@russlavbank.com")
  tAddrTo=("barry@russlavbank.com",)
  sMsg=""
  print "-----",strftime("%d.%m.%Y", localtime()),"-----"
  try:
    dbh=MySQLdb.Connect(host=dbServer,user=dbUser,passwd=dbPasswd,db=dbName)
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sSql="select * from %s where cResult<>'OK' and cDate=now()-INTERVAL 1 DAY" % tblName
    #print "Строка запроса: '%s'" % sSql
    cur.execute(sSql)
#    rs=cur.fetchallDict()
    for row in cur.fetchallDict():
      sMsg+="%s %s %s %s %s %s %s %s %s\n" %  (
        str(row['cDate']).split(" ")[0],  # выделяем только дату без времени
                                          # Python интерпретирует тип DATE как DATETIME :()
        row['cTime'], row['cIP'], row['cBID'], row['cLogin'], row['cTypeReq'],
        row['cRequest'], row['cResult'], row['cURL'])
    #print sMsg
    for i in xrange(0,len(tAddrTo)):
      ekSendmail(smtpServer, sAddrFrom, tAddrTo[i], "InetBank Log Viewer", sMsg)
      #print sMsg
    dbh.close()
  finally:
    print "Bye ;)"

if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
