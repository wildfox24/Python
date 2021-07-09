#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       balan.py
# Version:    1.0.7
# Purpose:    Send email with attach to list of recipients. List is stored in DB.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    26.11.2007
# Updated:   05.12.2007
# Copyright:  (c) 2007 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Send file to recipients by mail list stored in DB.
Run from cron.
'''
import sys, os, email, smtplib
import mimetypes
import MySQLdb
from time import localtime, strftime

sPath="/home/www/wwwrsb/files/balances/"
dbParam={'Server':'dbserver', 'DBName':'rsbcommon', 'Table':'RSBMailList', 'User':'webuser', 'Passwd':'Dt,>pth', 'Date':'000000'}
dMailParam={'Server':'10.0.1.17', 'From':'webmaster@russlavbank.com', 'To':'', 'Subject':'', 'File':''}

#---------------------------------------------------------------------------
def ekGetListOfRecipients(dbParam):
  retVal=[]
  #sSql="select * from %s where left(DT,'7')<'%s-%s' or left(DT,7)='0000-00'" % (dbParam["Table"], dbParam["Date"][:4],dbParam["Date"][4:6])
  sSql="select * from %s where left(DT,'7')<'%s-%s'" % (dbParam["Table"], dbParam["Date"][:4],dbParam["Date"][4:6])
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #print "Строка запроса: %s" % sSql
    cur.execute(sSql)
    res=cur.fetchall()
    retVal=[row for row in res]
    dbh.close()
  except MySQLdb.DatabaseError, tDetailError:
    print "ERROR: ", tDetailError.args
  return retVal
#---------------------------------------------------------------------------
def ekUpdateRecipient(dbParam, Recipient):
  sSql="update %s set DT=now() where Email='%s'" % (dbParam["Table"], Recipient)
  try:
    dbh=MySQLdb.Connect(host=dbParam["Server"],user=dbParam["User"],passwd=dbParam["Passwd"],db=dbParam["DBName"])
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #print "Строка запроса: %s" % sSql
    cur.execute(sSql)
    dbh.close()
  except MySQLdb.DatabaseError, tplDetailError:
    print "ERROR: ", tplDetailError.args
#---------------------------------------------------------------------------
def ekSendMailWithAttach(dMailParam):
  mainMsg=email.MIMEMultipart.MIMEMultipart()
  mainMsg['Subject']=dMailParam['Subject']
  mainMsg['From']=dMailParam['From']
  mainMsg['To']=dMailParam['To']
  mainMsg.preamble=""
  # Guarantees the message ends in a newline
  mainMsg.epilogue=''
  sText=u""
  msgTxt=email.MIMEText.MIMEText(sText)
  mainMsg.attach(msgTxt)

  ctype, encoding=mimetypes.guess_type(dMailParam['File'])
  if ctype is None or encoding is not None:
    # No guess could be made, or the file is encoded (compressed), so
    # use a generic bag-of-bits type.
    ctype='application/octet-stream'
  maintype, subtype=ctype.split('/', 1)
  fp=open(dMailParam['File'], 'rb')
  msgBin=email.MIMEBase.MIMEBase(maintype, subtype)
  msgBin.set_payload(fp.read())
  fp.close()
  # Encode the payload using Base64
  email.Encoders.encode_base64(msgBin)
  # Set the filename parameter
  Fname=os.path.basename(dMailParam['File'])
  msgBin.add_header('Content-Disposition', 'attachment', filename=Fname)
  mainMsg.attach(msgBin)
  try:
    smtpServer=smtplib.SMTP(host=dMailParam['Server'])
    smtpServer.sendmail(dMailParam['From'], dMailParam['To'], mainMsg.as_string())
    smtpServer.quit()
    print "Mail to: %s was sending" %  dMailParam['To']
  except smtplib.SMTPException, msgError:
    print "ERROR:", msgError
    return 0
  return 1
#---------------------------------------------------------------------------
def main():
  sFile=""
  dbParam['Date']=strftime("%Y%m", localtime())
  print "-----",strftime("%d.%m.%Y", localtime()),"-----"
  sFile=dbParam['Date']+".zip"
  if not os.path.exists(sPath+sFile):
    print "ERROR: File %s no exist..." %  sFile
    return -1 #No such file
  print "New file: ", sFile
  lRecipients=ekGetListOfRecipients(dbParam)
  #print lRecipients
  for Recipient in lRecipients:
    #print Recipient['ID'], Recipient['Email'], Recipient['DT']
    dMailParam['To']=Recipient['Email']
    dMailParam['Subject']="New balances from Russlavbank"
    dMailParam['File']=sPath+sFile
    if ekSendMailWithAttach(dMailParam):
      ekUpdateRecipient(dbParam, Recipient['Email'])
  return 0
  
if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
