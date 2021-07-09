#!/bin/env python
# -*- coding: cp1251 -*-
#----------------------------------------------------------------------------
# Name:       StatVirus.py
# Version:    1.0.3
# Получает на стандартный вход письмо с данными в формате CVS:
# Data;Time;Virus Name;IP address и заносит из в базу StatVirus.
# Данные отделяются от заголовка письма пустой строкой.
# Purpose:    Statistic Virus
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    25.03.2005
# Updated:    20.05.2005
# Copyright:  (c) 2004 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Get string from standard input,
Split it into items: Data, Time, Virus Name, IP-address
Input into database.
'''
import sys, getopt
from time import localtime, strftime
import MySQLdb

dbServer="dbserver"
dbName="DepSecurity"
tblName="StatVirus"
dbUser="statvirus"
dbPasswd="CnfnDbhec"
#---------------------------------------------------------------------------
def GetInput():
  sLine=sys.stdin.readline()
  while sLine[0]!="\n":
    sLine=sys.stdin.readline()
    continue
  sLine=sys.stdin.readline()
  return sLine.strip().split(";")
#---------------------------------------------------------------------------
def main():
  sSql=""
  arArgs=()
  arArgs=GetInput()
  try:
    dbh=MySQLdb.Connect(host=dbServer,user=dbUser,passwd=dbPasswd,db=dbName)
    cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sSql="INSERT INTO %s (cDate, cTime, cVName, cSIP) VALUES ('%s', '%s', '%s', '%s')" % (tblName,arArgs[0],arArgs[1],arArgs[2],arArgs[3])
    #print "Строка запроса: '%s'" % sSql
    cur.execute(sSql)
    dbh.close()
  finally:
    print "Bye ;)"

if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
