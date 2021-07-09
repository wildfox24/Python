#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekMakcFtpCopy.py
# Version:    0.1.0
# Purpose:    Get All files from /Агент/*, /Принципал/* from ftp://217.74.37.124.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    04.08.2017
# Updated:    07.08.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Get All files from /Агент/*, /Принципал/* from ftp://217.74.37.124.
Run from cron daily.
'''
import ftplib, sys, os
import datetime

curDate=datetime.date.today()
ftpServer="217.74.37.124"
ftpUser="maks"
ftpPass="kKjIUJBaQ"
ftpDirAgent="/Агент/"
ftpDirPrincipal="/Принципал/"
dstDirAgent="/home/Data/RSA"+ftpDirAgent
dstDirPrincipal="/home/Data/RSA"+ftpDirPrincipal

#---------------------------------------------------------------------------
def ekMakeTargetPath(tgPath):
	if os.path.isdir(tgPath):
		return 0
	else:
		os.makedirs(tgPath)
	
#---------------------------------------------------------------------------
def ekFtpGetFile(ftp, ftpDir, dstDir):
	dstPath=dstDir
	fn=0
	print dstPath
	try:
		ftp.cwd(ftpDir)
		dirs=ftp.nlst('*')
		#print dirs
		for d in dirs:
			print d+"/",
			for fl in ftp.nlst(d+"/*.xml"):
				#print fl
				if len(fl):
					f=fl.split("/")[1]
					print f
					ftp.retrbinary('RETR '+fl, open(dstPath+f, 'wb').write, 1024)
					fn+=1
		print "Files =", fn
	except ftplib.all_errors, error_msg:
		print error_msg
		return 1
	print "Dirs =", len(dirs)
	return 0
#---------------------------------------------------------------------------
def main():
	print "-----",curDate,"-----"
	print "Start files transfer..."
	curFtpDir=""
	curDstDir=""
	cmdArgs=len(sys.argv)
	print sys.argv
	if(len(sys.argv) > 1):
		cmdArgs=sys.argv[1]
		print cmdArgs
	try:
		ftp=ftplib.FTP(ftpServer)
		ftp.login(ftpUser, ftpPass)
	except ftplib.all_errors, msg:
		print msg
		return 1
	curDstDir=curDate.strftime("%Y%m%d/")	
	curFtpDir=ftpDirAgent+curDate.strftime("%Y/%m/%d/")
	#print curFtpDir
	ekMakeTargetPath(dstDirAgent+curDstDir+"arch")
	ekMakeTargetPath(dstDirAgent+curDstDir+"error")
	ekFtpGetFile(ftp, curFtpDir, dstDirAgent+curDstDir)
	
	curFtpDir=ftpDirPrincipal+curDate.strftime("%Y/%m/%d/")
	ekMakeTargetPath(dstDirPrincipal+curDstDir+"arch")
	ekMakeTargetPath(dstDirPrincipal+curDstDir+"error")
	ekFtpGetFile(ftp, curFtpDir, dstDirPrincipal+curDstDir)
	ftp.close()
	return 0
  
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
#
