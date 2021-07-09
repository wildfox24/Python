#!/bin/env python
#----------------------------------------------------------------------------
# Name:       ekMyAdmin.py
# Version:    1.0
# Purpose:    MySql admin tools
#
# Author:     Eugene Klepikov
# E-Mail:     klekfox@mail.ru
#
# Created:    12.10.2004
# Updated:    12.10.2004
# Copyright:  (c) 2004 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Хорошая прога ;)
'''
import sys, getopt
import gtk
from time import localtime, strftime
import smtplib
import MySQLdb

dbServer="dbserver"
dbName="InetBank"
dbUser="superdb"
dbPasswd="Cnfhsq Kbc"
tblName="InetBankLog"
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
def main():
  mainwin=gtk.Window(gtk.WINDOW_TOPLEVEL)
  mainwin.set_title(unicode("Прикольная прога","cp1251"))
  mainwin.set_default_size(300,200)
  mainwin.connect("destroy", lambda win: gtk.main_quit())
  mainwin.set_border_width(0)
  mainwin.show_all()
  gtk.main()
if __name__ == '__main__' : 
  sys.exit( main() )
#----------------------------------------------------------------------------
#
