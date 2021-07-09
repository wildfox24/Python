#!/bin/env python
# -*- coding: cp1251 -*-
#----------------------------------------------------------------------------
# Name:       mnav.py
# Version:    2.0.2
# Purpose:    Mail notify about virus
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    18.11.2004
# Updated:    12.05.2006
# Copyright:  (c) 2004 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Mail notify about virus.
Run from clamsmtpd
'''
import getopt, os, sys, smtplib
from time import localtime, strftime

import mimetypes

from email import Encoders
from email.Message import Message
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

smtpServer="localhost"
sAddrFrom="clamav@russlavbank.com"
sAddrTo=("virusbody@russlavbank.com",)
sAddrToNotify=("virus@russlavbank.com",)
sAddrToKasper=("virusbody@russlavbank.com","newvirus@kaspersky.com")
#sAddrFrom="clamav@slyfox.ru"
#sAddrTo=("virus@slyfox.ru",)
#sAddrToKasper=("virus@slyfox.ru","virus@slyfox.ru")
sMsg=""
dVirus={
        "Virus":"",
        "Sender":"",
        "Recipients":"",
        "Email":"",
        "TmpDir":"",
        "Zip":""
       }
#---------------------------------------------------------------------------
def ekSendMail(MailServer, MailFrom, MailTo, MailSubject, dMailMsg):
  mainMsg=MIMEMultipart()
  mainMsg['Subject']=MailSubject
  mainMsg['From']=MailFrom
  mainMsg['To']=",".join(MailTo)
  mainMsg.preamble=""
  # Guarantees the message ends in a newline
  mainMsg.epilogue=''
  
  sText="Virus: %s\nEmail: %s\nSender: %s\nRecipients: %s\n\nZIP pass 123\n\n" % \
       (dMailMsg['Virus'], dMailMsg['Email'], dMailMsg['Sender'], dMailMsg['Recipients'])
  msgTxt=MIMEText(sText)
  mainMsg.attach(msgTxt)

  ctype, encoding=mimetypes.guess_type(dMailMsg['Zip'])
  if ctype is None or encoding is not None:
    # No guess could be made, or the file is encoded (compressed), so
    # use a generic bag-of-bits type.
    ctype='application/octet-stream'
  maintype, subtype=ctype.split('/', 1)
  fp=open(dMailMsg['Zip'], 'rb')
  msgBin=MIMEBase(maintype, subtype)
  msgBin.set_payload(fp.read())
  fp.close()
  # Encode the payload using Base64
  Encoders.encode_base64(msgBin)
  # Set the filename parameter
  Fname=os.path.basename(dMailMsg['Zip'])
  msgBin.add_header('Content-Disposition', 'attachment', filename=Fname)
  mainMsg.attach(msgBin)
  try:
    smtpServer=smtplib.SMTP(host=MailServer)
    for MailToItem in MailTo:
      #print "Send mail to: ", MailToItem
      smtpServer.sendmail(MailFrom, MailToItem, mainMsg.as_string())
    smtpServer.quit()
  except:
    print "ERROR: send mail failure"
    
#---------------------------------------------------------------------------
def ekSendNotifyMail(MailServer, MailFrom, MailTo, dMailMsg):
  sText="Virus: %s\nEmail: %s\nSender: %s\nRecipients: %s\n\n" % \
       (dMailMsg['Virus'], dMailMsg['Email'], dMailMsg['Sender'], dMailMsg['Recipients'])
  try:
    smtpServer=smtplib.SMTP(host=MailServer)
    for MailToItem in MailTo:
      #print "Send mail to: ", MailToItem
      mailMsg = """Subject: Clamsmtp found virus! \nFrom: %s\nTo: %s\nMIME-Version: 1.0\nContent-Type: text/plain;charset="Windows-1251"\n\n%s""" % (MailFrom, MailToItem, sText)
      smtpServer.sendmail(MailFrom, MailToItem, mailMsg)
    smtpServer.quit()
  except smtplib.SMTPException:
    print "ERROR:", tplDetailError.args
    
#---------------------------------------------------------------------------
def main():
  try:
#    dVirus['Virus']="HTML.Phishing.Bank-255"
    dVirus['Virus']=os.getenv('VIRUS')
    dVirus['Email']=os.getenv('EMAIL')
#    dVirus['Zip']="/usr/local/bin/1.zip"
    dVirus['Zip']=os.getenv('EMAIL')+".zip"
    dVirus['Sender']=os.getenv('SENDER')
    dVirus['Recipients']=os.getenv('RECIPIENTS')
    sCmd="zip -P %s %s %s" % ("123", dVirus['Zip'], dVirus['Email'])
    os.popen(sCmd)
#    if(dVirus["Virus"].find("Phishing")!=-1):
#      ekSendMail(smtpServer, sAddrFrom, sAddrToKasper, "Clamsmtp found virus!", dVirus)
#    else: 
      ekSendMail(smtpServer, sAddrFrom, sAddrToKasper, "Clamsmtp found virus!", dVirus)
#      ekSendMail(smtpServer, sAddrFrom, sAddrTo, "Clamsmtp found virus!", dVirus)
    ekSendNotifyMail(smtpServer, sAddrFrom, sAddrToNotify, dVirus)
  finally:
    os.chmod(dVirus['Email'],0664)
    os.unlink(dVirus['Email'])
    os.unlink(dVirus['Zip'])
    print "\nDone ;)"
  return 0

if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
