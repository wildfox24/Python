#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       delexpfile.py
# Version:    1.0.5
# Purpose:    Delete expired files in directory.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    10.01.2008
# Updated:    17.03.2009
# Copyright:  (c) 2008 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Delete expired files in directory.
Run from cron daily.
'''
import sys, os, datetime
from stat import *
iExpDays=30
dtToday=datetime.date.today()
sPath="/home/www/wwwrsb/files"
arExcludeDirs=('balances', 'bic_reference', 'cashdesk', 'csupport', 'prcenter', 'const')
#---------------------------------------------------------------------------
def ekDelExpFiles(Path):
  dtFile=0
  sPathFile=""
  for file in os.listdir(Path):
    sPathFile=os.path.join(Path, file)
    dtFile=datetime.date.fromtimestamp(os.stat(sPathFile)[ST_ATIME])
    #print "Path: ", sPathFile, dtFile.strftime("%d.%m.%Y")
    if(os.path.isdir(sPathFile)):
      if file in arExcludeDirs: continue
      #print "Path is dir: ", sPathFile, datetime.date.fromtimestamp(os.stat(sPathFile)[ST_CTIME])
      ekDelExpFiles(sPathFile)
    dtDiff=dtToday-dtFile
    if(dtDiff.days > iExpDays):
       try:
         if(os.path.isdir(sPathFile)):
           print "Delete Directory: ", sPathFile, datetime.date.fromtimestamp(os.stat(sPathFile)[ST_ATIME])
           os.rmdir(sPathFile)
         else:
          print "Delete File: ", sPathFile, datetime.date.fromtimestamp(os.stat(sPathFile)[ST_ATIME])
          os.unlink(sPathFile)
       except OSError, msgError:
         print msgError
  return 0
#---------------------------------------------------------------------------
def main():
  print "-----",dtToday.strftime("%d.%m.%Y"),"-----"
  ekDelExpFiles(sPath)
  return 0
  
if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
