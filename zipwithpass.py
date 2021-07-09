#!/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       zipwithpass.py
# Version:    1.0.0
# Purpose:    Zip file with password
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    08.06.2005
# Updated:    08.06.2005
# Copyright:  (c) 2005 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
'''
import os, sys
#---------------------------------------------------------------------------

def main():
  try:
    sCmd="zip -P %s %s %s" % ("123", "123", "1.doc")
    os.popen(sCmd)
  finally:
    print "\nDone ;)"
  return 0

if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
