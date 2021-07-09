#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekpvufadp.py
# Version:    1.0
# Purpose:    Backup PVU Adapter files.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    09.12.2017
# Updated:    12.12.2017
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Backup PVU Adapter files
'''
import sys, os
import datetime

dirSrc="/mnt/adp-106/ClientFiles/Arch/fromRSA/"
dirDst="/home/Data/adp-106/"
workDate=datetime.date.today()-datetime.timedelta(1)
delDate=datetime.date.today()-datetime.timedelta(15)
#curDir=workDate.strftime("%Y/%m/%d/")
curDir=workDate.strftime("%Y/")
delDir=delDate.strftime("%Y/%m/%d/")

cmdScan="rsync -auv "+dirSrc+curDir+" "+dirDst+curDir
os.system(cmdScan)
print cmdScan
cmdDel="rm -rf "+dirSrc+delDir
os.system(cmdDel)
print cmdDel
