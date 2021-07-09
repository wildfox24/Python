#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekRstDBarch.py
# Version:    1.0
# Purpose:    Restore dbarchive to reserv dbs
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    06.07.2021
# Updated:    08.07.2021
# Copyright:  (c) 2021 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
Restore db archives to reserv servers
'''
import sys, os, subprocess
import datetime
cmd=""
host={'makcdb-reserv':'172.20.22.61',
      'intra-reserv':'172.20.22.55'}
db_name=['b2b', 'b2b_system', 'dms', 'dms_dev', 'dms_online_belgorod', 'dms_online_belgorod_dev',
         'dms_online_tomsk', 'dms_online_tomsk_dev', 'DMS_Policies', 'DMS_Policies_dev',
         'garmoniya', 'logs', 'other', 'sbroker', 'sbroker_dev', 'services', 'sessions', 'valutes',
         'makc', 'intranet']
dbuser="sadmin"
dbpasswd="trep@let_dba"
curDate=datetime.date.today()
fprefix="makc-mysql-{0:02d}-{1:02d}-{2:04d}".format(curDate.day, curDate.month, curDate.year)

#---------------------------------------------------------------------------
def UsageInfo():
	print("Usage info:")
	print("ekRstDBarch.py <dbhost>")
	print("dbhosts: makcdb-reserv, intra-reserv")
#---------------------------------------------------------------------------

def main():
	#print(sys.argv)
	if(len(sys.argv) > 1):
		dbhost=sys.argv[1]
	else:
		UsageInfo()
		exit()

	print("-----",curDate,"-----")
	for i in range(0,len(db_name)):
		cmd="mysql -h{0:s} -u{1:s} -p'{2:s}' {3:s} < {4:s}.{5:s}".format(host[dbhost], dbuser, dbpasswd, db_name[i], fprefix, db_name[i]) 
		print(cmd)
		retval=os.system(cmd)
	
if __name__ == '__main__' :
	sys.exit( main() )
#----------------------------------------------------------------------------
