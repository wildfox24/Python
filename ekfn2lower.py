#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekfn2lower.py
# Version:    0.0.1
# Purpose:    Convert file name to lower case.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    16.01.2009
# Updated:   16.01.2009
# Copyright:  (c) 2009 Klek
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Convert file name to lower case
'''
import os
import sys
from time import localtime, strftime

path="/home/klek/temp/best/"
#path="/media/40Gb/Media/Audio/best/"
#path="/home/klek/temp/Песня Года 2008/"
fnlist=os.listdir(path)

#---------------------------------------------------------------------------
def main():
    curDate=strftime("%d.%m.%Y", localtime())
    print "-----",curDate,"-----\n"
    for i in xrange(0,len(fnlist)):
        oldname=fnlist[i].decode('utf-8')
        newname=oldname.lower()
        poldname=path.decode('utf-8') + oldname
        pnewname=path.decode('utf-8') + newname
        os.rename(poldname, pnewname)
        print pnewname
    print i

#---------------------------------------------------------------------------
if __name__ == '__main__' :
  sys.exit( main() )

#----------------------------------------------------------------------------
#
