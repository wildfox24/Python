#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekrsaftpcp.py
# Version:    1.6.0
# Purpose:    Get All files from /Агент/*, /Принципал/* from ftp://217.74.37.124.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    04.08.2017
# Updated:    15.08.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Get All files from dirs /Агент/*, /Принципал/* from RSA tp://217.74.37.124.
Run from cron daily.
'''
import ftplib, sys, os
import datetime
import re

workDate=datetime.date.today()
ftpServer="217.74.37.124"
ftpUser="maks"
ftpPass="kKjIUJBaQ"
ftpDirAgent="/Агент/"
ftpDirPrincipal="/Принципал/"
dstDirAgent="RSA/Agent/"
dstDirPrincipal="RSA/Principal/"

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
	#print ftpDir
	try:
		ftp.cwd(ftpDir)
		dirs=ftp.nlst()
		print ftp.pwd()
		#print dirs
		for d in dirs:
			fs=d+'/'+d+'.xml'
			dstPath=dstDir+d+'.xml'
			try:
			    ftp.retrbinary('RETR '+fs, open(dstPath, 'wb').write)
			    print fs
			    fn+=1
			except ftplib.error_perm, msg:
			    print msg

		print "Files =", fn
	except ftplib.all_errors, error_msg:
		print error_msg
		return 1
	print "Dirs =", len(dirs)
	return 0
#---------------------------------------------------------------------------
def main():
	global workDate
	print "-----",workDate,"-----"
	print "Start files transfer..."
	curFtpDir=""
	curDstDir=""
	cmdArgs=len(sys.argv)
	print sys.argv
	if(len(sys.argv) > 1):
		cmdArgs=re.split("[-.,/]", sys.argv[1])
		if(len(cmdArgs[0])==4):
			workDate=datetime.date(int(cmdArgs[0]), int(cmdArgs[1]), int(cmdArgs[2]))
		else:
			workDate=datetime.date(int(cmdArgs[2]), int(cmdArgs[1]), int(cmdArgs[0]))

		print workDate

	try:
		ftp=ftplib.FTP(ftpServer)
		ftp.login(ftpUser, ftpPass)
		ftp.set_pasv(0)
		ftp.set_debuglevel(0)

	except ftplib.all_errors, msg:
		print msg
		return 1
	curDstDir=workDate.strftime("%Y%m%d/")	
	curFtpDir=ftpDirAgent+workDate.strftime("%Y/%m/%d/")
	#print curFtpDir
	ekMakeTargetPath(dstDirAgent+curDstDir+"arch")
	ekMakeTargetPath(dstDirAgent+curDstDir+"error")
	ekFtpGetFile(ftp, curFtpDir, dstDirAgent+curDstDir)
	
	curFtpDir=ftpDirPrincipal+workDate.strftime("%Y/%m/%d/")
	ekMakeTargetPath(dstDirPrincipal+curDstDir+"arch")
	ekMakeTargetPath(dstDirPrincipal+curDstDir+"error")
	ekFtpGetFile(ftp, curFtpDir, dstDirPrincipal+curDstDir)
	ftp.close()
	return 0
  
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
#
