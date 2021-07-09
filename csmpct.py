#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       csmpct.py
# Version:    1.0.3
#
# Contact System payment points by metro stations common table
# 
#
# Purpose:    CBR Rate of Exchange
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    01.02.2010
# Updated:    01.02.2010
# Copyright:  (c) 2005 KlekFox
# Licence:    GPL
#
# Set correct value sEncoding to your system encoding
#
#----------------------------------------------------------------------------
##
'''
insert into Metro_Payment_Spr
select distinct NULL, m.city, m.metro, c.ProductID, c.Name, m.PP_CODE
from CRM_Product c, PP_SERVICES_4_WWW w, PP_SENDERS_2_COMPANY_4_WWW s, PP_BANK_METRO_INFO m
where c.ProductID = w.Service_ID
and w.PP_CODE = s.REC_CODE
and s.SENDER_CODE = m.PP_CODE
order by c.Name, m.PP_CODE
'''
import sys
import datetime
import MySQLdb

sEncoding="cp1251"
dbServer="dbserver"
dbName="ContactSystem"
tblName="Metro_Payment_Spr"
dbUser="superdb"
dbPasswd="Cnfhsq Kbc"
#---------------------------------------------------------------------------

def main():
  sql = """
        insert into Metro_Payment_Spr
        select distinct NULL, m.city, m.metro, c.ProductID, c.Name, m.PP_CODE
        from CRM_Product c, PP_SERVICES_4_WWW w, PP_SENDERS_2_COMPANY_4_WWW s, PP_BANK_METRO_INFO m
        where c.ProductID = w.Service_ID
        and w.PP_CODE = s.REC_CODE
        and s.SENDER_CODE = m.PP_CODE
        order by c.Name, m.PP_CODE
        """
  #sql_drop = "truncate table %s" % tblName
  sql_drop = "delete from %s" % tblName
  dt = datetime.datetime.now()
  revdt = dt.strftime("%Y-%m-%d")

  print "-----",dt.strftime("%d.%m.%Y"),"-----\n"

  try:
      dbh=MySQLdb.Connect(host=dbServer,user=dbUser,passwd=dbPasswd,db=dbName)
      cur=dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
      print "Delete data from %s Table:" % tblName
      cur.execute(sql_drop)
      print "Done with %d rows;)\n" % cur.rowcount
      print "Insert data into %s Table:" % tblName
      cur.execute(sql)
      print "Done with %d rows;)\n" % cur.rowcount
      dbh.close()
  except MySQLdb.DatabaseError, tplDetailError:
      print "ERROR:", tplDetailError.args

  else:
    print "Done ;)\n"

#---------------------------------------------------------------------------
if __name__ == '__main__' :
  sys.exit( main() )

#----------------------------------------------------------------------------
#
