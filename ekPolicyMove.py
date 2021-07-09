#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekPolicyMove.py
# Version:    1.5.2
# Purpose:    Move Policy files (pdf, sig) to backup server.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    28.12.2016
# Updated:    30.12.2016
# Copyright:  (c) 2016 WildFox
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Move Policy files (pdf & sig) to backup server
Run from cron daily.
'''

import os, sys
import datetime
import shutil

#curDate=datetime.date(2016,12,27)
curDate=datetime.date.today()
srcPath='/home/bitrix/www/new/market/calculators/'
#srcPath="/home/klek/Projects/calculators/"
#osago/print_policy/'
dstPath="/mnt/backup_policy/calculators/"
#dstPath="/tmp/backup_policy/calculators/"
policyPath="/print_policy/"
lstCalcs=["antivirus", "antivirus-iframe", "casco", "children_camp", "children_camp-iframe", "city_lights",
"dms-migrant", "dms-migrant-online", "dms_online", "express", "express-iframe", "family_home", "farewell",
"farewell-iframe", "flatvoyage", "flatvoyage_ab", "garmoniya", "garmoniya-iframe", "ipoteka", "keb",
"neposeda", "neposeda-iframe", "osago", "osago_mm", "persona", "persona-iframe", "rinda", "summer_rest",
"to_start", "to_start-iframe", "vzr", "vzr-iframe"]

#---------------------------------------------------------------------------
def ekMakeDir(sDir):
	
	try:
		os.makedirs(sDir)
	except OSError, msgError:
		#print msgError
		pass
	return 0
	
#---------------------------------------------------------------------------
def ekMoveFiles(calcPath):
	files=[]
	fullPath=srcPath+calcPath+policyPath
	
	try:
		files=os.listdir(fullPath)
	except OSError, msgError:
		print msgError

	for file in files:
		fPath=os.path.join(fullPath,file)
		dtFile=datetime.date.fromtimestamp(os.path.getmtime(fPath))
		dtDiff=dtFile-curDate
		if(dtDiff.days < 0):
			dstFullPath=dstPath+calcPath+"/"+str(dtFile.year)+"/"+str(dtFile.month)
			#print dtFile,dtDiff,fPath
			ekMakeDir(dstFullPath)
			try:
				shutil.move(fPath, dstFullPath)
 				#shutil.copy2(fPath, dstFullPath)
			except shutil.Error, msgError:
				print msgError
				#pass
	#print fullPath
	#print dstFullPath
	return 0
	
#---------------------------------------------------------------------------
def main():
	print "-----",curDate,"-----"
	print "Start files moving..."
	#print len(lstCalcs)
	for calc in lstCalcs:
		print "Processing {0}...".format(calc,)
		#calc="osago"
		ekMoveFiles(calc)
	print "Finish."
	return 0
  
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
#
