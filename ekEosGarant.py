#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekeosgarant.py
# Version:    1.3
# Purpose:    Backup Eosago-Garant files.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    06.12.2017
# Updated:    07.12.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Backup Eosago-Garant files
'''
import sys, os
import datetime

ScanSrc="/mnt/Garant-Eosg/app/log/scan/"
ScanDst="/mnt/Eosg-Garant/scan/"
DocsSrc="/mnt/Garant-Eosg/app/log/"
DocsDest="/mnt/Eosg-Garant/docs/"
#Yesterday
workDate=datetime.date.today()-datetime.timedelta(1)
curDir=workDate.strftime("%Y/%m/%d/")

cmdScan="rsync -auv /mnt/Garant-Eosg/app/log/scan/"+curDir+" /mnt/Eosg-Garant/scan/"+curDir
cmdDocs="rsync -auv /mnt/Garant-Eosg/app/log/"+curDir+" /mnt/Eosg-Garant/docs/"+curDir
os.system(cmdScan)
print cmdScan
os.system(cmdDocs)
print cmdDocs
