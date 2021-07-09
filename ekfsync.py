#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekfsync.py
# Version:    1.1
# Purpose:    Synchronisation dirs
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    19.02.2020
# Updated:    20.02.2020
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Sync /home/oracle/disk2/car_photo/integration_file/ from arzamas to kissamos
'''
import sys, os, subprocess
import datetime
wd=0
cmd=""
fname="/home/oracle/ekfsync.dat"
#fname="ekfsync.dat"

curDate=datetime.date.today()
#---------------------------------------------------------------------------

def ekGetData(fname):
	with open(fname, "rt") as f:
		for line in f:
			data=(int(line.strip()))
			#print(data)
	return int(data)
#---------------------------------------------------------------------------

def ekWriteData(fname, data):
	with open(fname, "wt") as f:
		f.write(data)

	
#---------------------------------------------------------------------------

def main():
	print "-----",curDate,"-----"
	wd=ekGetData(fname)
	cmd="rsync -auv /home/oracle/disk2/car_photo/integration_file/{0:04d}/ /mnt/cph/integration_file/{1:04d}/ | wc -l".format(wd, wd)
	print cmd
	retval=subprocess.check_output(cmd, shell=True)
	if int(retval) == 4:
		print "Change to next dir {0:04d}".format(wd+1)
		ekWriteData(fname, str(wd+1))
	print retval
	return 0
	
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
