#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ektwitnews.py
# Version:    1.0.3
#
# Get News from BD and sent to twitter account
#
# Purpose:    Twit news
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    18.03.2010
# Updated:    26.05.2010
# Copyright:  (c) 2010 KlekFox
# Licence:    GPL
#
# Set correct value sEncoding to your system encoding
#
#----------------------------------------------------------------------------
##
'''
Twit News
'''
import sys
from time import localtime, strftime
import MySQLdb
import urllib2
import twitter

db_params = {'server': 'dbserver',
             'name': 'wwwrsb',
             'user': 'wwwrsb',
             'passwd': 'hEccKfd<fyr',
             'table': 'News',
             'encoding': 'cp1251'}
base_url = "http://www.russlavbank.com/prcenter/news/"
users = [['russlavbank', 'eke08j3NFiuPM'],
               ['contact_sys', 'rnPsW6dJN5vXY']]

#---------------------------------------------------------------------------

def get_shorten_url(url):
    u = urllib2.urlopen('http://clck.ru/--?url=' + url)
    shorten_url = u.read()
    return shorten_url
#---------------------------------------------------------------------------

def post_to_twitter(user='', passwd='', status=''):
    api = twitter.Api(username=user, password=passwd)
    status = api.PostUpdate(status)
    return status 
#---------------------------------------------------------------------------

def get_articles():
    articles=[]
    try:
        dbh = MySQLdb.Connect(host=db_params['server'], user=db_params['user'], passwd=db_params['passwd'], db=db_params['name'])
        cur = dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from %s  where IsTwitted='0' order by DT Asc" % (db_params['table'])
        cur.execute(sql)
        #row = cur.fetchone()
        for row in cur.fetchall():
            articles.append([row['ID'], row['DT'], row['Header'].decode('cp1251')])
        dbh.close()
    except MySQLdb.DatabaseError, tplDetailError:
        print "ERROR:", tplDetailError.args
    return articles
#---------------------------------------------------------------------------

def set_article_twitted(recID):
    retval = 0
    try:
        dbh = MySQLdb.Connect(host=db_params['server'], user='swwwrsb', passwd='cEgtH hEccKfd<fyr', db=db_params['name'])
        cur = dbh.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "update %s set IsTwitted=1 where ID=%d" % (db_params['table'], recID)
        #print "Строка запроса: '%s'" % sql
        cur.execute(sql)
        row = cur.fetchone()
        dbh.close()
    except MySQLdb.DatabaseError, tplDetailError:
        print "ERROR:", tplDetailError.args
        retval = 1
    return retval 
#---------------------------------------------------------------------------

def main():
    msg=""
    sDate = strftime("%d.%m.%Y", localtime())
    sRevDate = strftime("%Y-%m-%d", localtime())
    print "-----",sDate,"-----\n"
    print "Send to Twitter: "
    for article in get_articles():
        url="%s%s.html" % (base_url, article[0],)
        surl=get_shorten_url(url)
        msg="%s %s" % (article[2], surl,)
        #pass
        print post_to_twitter(user=users[0][0], passwd=users[0][1], status=msg).text
        set_article_twitted(article[0])
    print "\nDone ;)"
#---------------------------------------------------------------------------

if __name__ == '__main__' :
    sys.exit( main() )
#----------------------------------------------------------------------------
#
