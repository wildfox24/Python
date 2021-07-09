#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       fcp1251.py
# Version:    1.0.1
# Purpose:    Replace microsoft-cp1252 with microsoft-cp1251 in fonts.dir and fonts.scale
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    30.11.2005
# Updated:    15.02.2006
# Copyright:  (c) 2005 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
##
'''
Make correct cp1251 rule in fonts.dir and fonts.scale.
Replace windows-cp1252 with windows-cp1251
'''
import sys

Pathes=['/usr/X11/lib/X11/fonts/msfonts',
             '/usr/X11/lib/X11/fonts/msfonts-style',
             '/usr/X11/lib/X11/fonts/msfonts-style',
             '/usr/X11/lib/X11/fonts/truetype',
             '/usr/X11/lib/X11/fonts/URW',
             '/usr/X11/lib/X11/fonts/Type1',
             '/usr/X11/lib/X11/fonts/msfonts-style',
             #'.'
             ]
#---------------------------------------------------------------------------
def fontReplace(file):
    print file
    fin=open(file, 'r')
    fonts=fin.readlines()
    fin.close()
    try:
        fout=open(file, 'w')
        for line in fonts:
            #if line.count('cp1252'):
                #line.replace('cp1252', 'cp1251')
            #print line.replace('cp1252', 'cp1251')
            fout.write(line.replace('cp1252', 'cp1251'))
        fout.close()
    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
  
#---------------------------------------------------------------------------
def main():
    for path in Pathes:
        fontReplace(path+'/fonts.dir')
        fontReplace(path+'/fonts.scale')
    print "--- END ---"

#---------------------------------------------------------------------------
if __name__ == '__main__' :
   sys.exit(main())
