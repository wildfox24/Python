#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekeosgarantdel.py
# Version:    1.2
# Purpose:    Delete Eosago-Garant files.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    07.12.2017
# Updated:    05.02.2018
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Delete Eosago-Garant files
'''
import sys, os
import datetime

ScanSrc="/mnt/Garant-Eosg/app/log/scan/"
DocsSrc="/mnt/Garant-Eosg/app/log/"
ScanDst="/mnt/Eosg-Garant/scan/"
DocsDst="/mnt/Eosg-Garant/docs/"

# Today -2
workDate=datetime.date.today()-datetime.timedelta(2)
curDir=workDate.strftime("%Y/%m/%d/")
#print curDir
cmdScan="rm -rf /mnt/Garant-Eosg/app/log/scan/"+curDir
cmdDocs="rm -rf /mnt/Garant-Eosg/app/log/"+curDir
if os.path.exists(ScanDst+curDir):
    os.system(cmdScan)
    print cmdScan
if os.path.exists(DocsDst+curDir):
    os.system(cmdDocs)
    print cmdDocs
