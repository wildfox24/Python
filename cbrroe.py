#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       cbrroe.py
# Version:    1.0.9
#
# Get XML document from XML web-service www.cbr.ru,
# Parse it and insert into database.
#
# Purpose:    CBR Rate of Exchange
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    14.04.2005
# Updated:    13.03.2009
# Copyright:  (c) 2005 KlekFox
# Licence:    GPL
#
# Set correct value sEncoding to your system encoding
#
#----------------------------------------------------------------------------
##
'''
Get XML document from XML web-service www.cbr.ru,
Parse it and insert into database.
'''
import sys
from time import localtime, strftime
import MySQLdb
import urllib
import xml.dom.minidom

sEncoding="cp1251"
dbServer="dbserver"
dbName="rsbcommon"
tblName="CBRExchange"
dbUser="rsbcombot"
dbPasswd="Rbylpvfhfekb"
#---------------------------------------------------------------------------
def ekGetInput(sDate):
  sURL="http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s" % (sDate)
  prxy={"http":"http://10.0.1.218:8686"}
  #u=urllib.urlopen(sURL, proxies=prxy)
  u=urllib.urlopen(sURL)
  return u.read()

#---------------------------------------------------------------------------
def ekParseXMLDoc(xmlDoc):
  lstDicXMLNodes=[]
  dicXMLNodes={}
  xmldoc=xml.dom.minidom.parseString(xmlDoc)
  root=xmldoc.documentElement
  for valute in root.childNodes:
    if valute.nodeName=='#text':
      continue
    for ch in valute.childNodes:
      if ch.nodeName=='#text': # Drop TextNode, that is means "\n" in the xml document
        continue
      dicXMLNodes[ch.nodeName]=ch.childNodes[0].nodeValue
    lstDicXMLNodes.append(dicXMLNodes)
    dicXMLNodes={}
  return lstDicXMLNodes

#---------------------------------------------------------------------------
def main():
  sSql=""
  lstDicXMLNodes=()
  sDate=strftime("%d.%m.%Y", localtime())
  sRevDate=strftime("%Y-%m-%d", localtime())
  #sDate="29.10.2008"
  #sRevDate="2008-10-29"
  print "-----",sDate,"-----\n"
  lstDicXMLNodes=ekParseXMLDoc(ekGetInput(sDate))
  try:
    for dicXMLNode in lstDicXMLNodes:
      dbh=MySQLdb.Connect(host=dbServer,user=dbUser,passwd=dbPasswd,db=dbName)
      cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
      sSql="INSERT INTO %s (Date, NumCode, CharCode, Nominal, Name, Value) values('%s', '%d', '%s', '%d', '%s', '%9.4f')" % \
           (tblName, sRevDate, int(dicXMLNode['NumCode']), dicXMLNode['CharCode'].encode(sEncoding), int(dicXMLNode['Nominal']), \
            dicXMLNode['Name'].encode(sEncoding), float(dicXMLNode['Value'].replace(",",".")))
      print "Строка запроса: '%s'" % sSql
      cur.execute(sSql)
      dbh.close()
  except MySQLdb.DatabaseError, tplDetailError:
      print "ERROR:", tplDetailError.args

  else:
    print "\n\nDone ;)"

#---------------------------------------------------------------------------
if __name__ == '__main__' :
  sys.exit( main() )

#----------------------------------------------------------------------------
#
