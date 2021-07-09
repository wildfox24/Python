#!/usr/bin/env python
# -*- coding: utf8 -*-
#----------------------------------------------------------------------------
# Name:       ekchwlp.py
# Version:    1.0.4.1
# Purpose:    Change desktop wallpaper.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    16.07.2012
# Updated:    23.07.2012
# Copyright:  (c) 2012 KlekFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Change Desktop wallpaper.
Get list of pictures.
Randomly set as desktop background picture.
'''
import sys, os, glob, random
from time import localtime, strftime

path="/home/klek/Pictures/wallpapers/"

#---------------------------------------------------------------------------
def ekGetFileList(Path):
  lFiles=[]
  for fname in os.listdir(path):
    if os.path.isfile(path+fname):
    	 #print fname
    	 lFiles.append(fname)
  return lFiles
#---------------------------------------------------------------------------
def main():
  flist=[]
  curTime=strftime("%d.%m.%Y %H:%M:%S", localtime())
  print "-----",curTime,"-----"
  flist=ekGetFileList(path)
  flist.sort()
  #flist.reverse()
  randItem=random.randint(0,len(flist)-1)
  cmd="gsettings set org.gnome.desktop.background picture-uri 'file://%s%s'" % (path,flist[randItem],)
  try:
    print "Random file: %s" % cmd
    os.system(cmd)
    print 'Done'
  except:
    return -1
  return 0
  
if __name__ == '__main__' :
  sys.exit( main() )
#----------------------------------------------------------------------------
#
