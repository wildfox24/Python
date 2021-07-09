#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekrsaftpcp2.py
# Version:    1.2.5
# Purpose:    Get All files from /Агент/*, /Принципал/* from ftp://217.74.37.124.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    04.08.2017
# Updated:    14.11.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Get All files from dirs /Агент/*, /Принципал/* from RSA tp://217.74.37.124.
Run from cron daily.
'''
import pycurl
import sys, os
import datetime
import re
from io import BytesIO

workDate=datetime.date.today()
ftpServer="ftp://10.0.136.1"
ftpUser="maks:kKjIUJBaQ"
#ftpUrl="ftp://maks:kKjIUJBaQ@217.74.37.124/"
ftpUrl="ftp://10.0.136.1/"
ftpDir=["Агент/", "Принципал/"]
dstDir=["o:/RSA/Agent/","o:/RSA/Principal/"]

#---------------------------------------------------------------------------
def ekMakeTargetDirs(path):
	if os.path.isdir(path):
		return 0
	else:
		os.makedirs(path)
	
#---------------------------------------------------------------------------
def ekGetFile(fpath, fname, dstdir):
	url=fpath+'/'+fname
	dstPath=workDate.strftime("%Y%m%d/")	
	dstfile=dstdir+dstPath+fname
	print dstfile
	fp=open(dstfile, 'wb')
	curl=pycurl.Curl()
	curl.setopt(curl.URL, url)
	curl.setopt(curl.USERPWD, ftpUser)
	curl.setopt(curl.WRITEDATA, fp)
	curl.setopt(curl.CONNECTTIMEOUT, 30)
	curl.setopt(curl.TIMEOUT, 300)
	try:
		curl.perform()
	except pycurl.error, msg:
		print msg
	fp.close()
	curl.close()
	return 0
#---------------------------------------------------------------------------
def ekGetDirs(ftpPath, dstDir):
	lstDir=[]
	dl=BytesIO()
	url=ftpUrl+ftpPath
	print url
	curl=pycurl.Curl()
	curl.setopt(curl.URL, url)
	curl.setopt(curl.USERPWD, ftpUser)
	curl.setopt(curl.WRITEFUNCTION, dl.write)
	curl.setopt(curl.CONNECTTIMEOUT, 30)
	curl.setopt(curl.TIMEOUT, 300)
	try:
		curl.perform()
		ds=dl.getvalue().split('\n')
		#print ds
	except pycurl.error, msg:
		print msg
	curl.close()
	for i in range(0, len(ds)-1):
		lstDir.append(ds[i].split()[8])
		ekGetFile(url+ds[i].split()[8], ds[i].split()[8]+'.xml', dstDir)
	print len(ds), len(lstDir)
	return lstDir
#---------------------------------------------------------------------------
def main():
	global workDate
	print "-----",workDate,"-----"
	print "Start files transfer..."
	ftpPath=""
	dstPath=""
	cmdArgs=len(sys.argv)
	print sys.argv
	if(len(sys.argv) > 1):
		cmdArgs=re.split("[-.,/]", sys.argv[1])
		if(len(cmdArgs[0])==4):
			workDate=datetime.date(int(cmdArgs[0]), int(cmdArgs[1]), int(cmdArgs[2]))
		else:
			workDate=datetime.date(int(cmdArgs[2]), int(cmdArgs[1]), int(cmdArgs[0]))
		print workDate
	for i in range(0, len(ftpDir)):
		dstPath=workDate.strftime("%Y%m%d/")	
		ftpPath=ftpDir[i]+workDate.strftime("%Y/%m/%d/")
		ekMakeTargetDirs(dstDir[i]+dstPath+"arch")
		ekMakeTargetDirs(dstDir[i]+dstPath+"error")
		ekGetDirs(ftpPath, dstDir[i])
	return 0
  
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
#
