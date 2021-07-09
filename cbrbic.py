#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       cbrbic.py
# Version:    0.9.1
#
# Get XML document from XML web-service www.cbr.ru,
# Parse it and insert into database.
#
# Purpose:    Get CBR BIC files
#
# Author:     Eugene Klepikov
# E-Mail:     klek@hotmail.ru
#
# Created:    29.11.2011
# Updated:    20.12.2011
# Copyright:  (c) 2011 KlekFox
# Licence:    GPL
#
#
#----------------------------------------------------------------------------
##
'''
Get XML document from XML web-service www.cbr.ru,
Parse it and download certain files.
'''
import sys, os
from time import localtime, strftime
import urllib
import xml.dom.minidom

urlXmlDoc="http://cbr.ru/mcirabis/PluginInterface/GetBicCatalog.aspx"
urlBicFile="http://cbr.ru/mcirabis/BIK/"
saveDir="/home/www/files/cbrbic/"
#---------------------------------------------------------------------------
def ekGetFile(sURL):
    prxy={"http":"http://10.0.1.218:8686"}
    #u=urllib.urlopen(sURL, proxies=prxy)
    u=urllib.urlopen(sURL)
    return u.read()

#---------------------------------------------------------------------------
def ekParseXMLDoc(xmlDoc, Date):
    dicItemAttr={}
    dicChAttr={}
    dicFiles={"full":"", "correct":""}
    xmldoc=xml.dom.minidom.parseString(xmlDoc)
    items=xmldoc.getElementsByTagName("item")
    for item in items:
        #print "%s" % item.nodeName
        for i in xrange(0,item.attributes.length):
            dicItemAttr[item.attributes.item(i).name]=item.attributes.item(i).value
        if dicItemAttr['date'] == Date:
            #print "Date=%s File=%s" % (dicItemAttr['date'], dicItemAttr['file'])
            dicFiles['date']=dicItemAttr['date']
            dicFiles['full']=dicItemAttr['file']
            for ch in item.childNodes:
                for k in xrange(0,ch.attributes.length):
                    dicChAttr[ch.attributes.item(k).name]=ch.attributes.item(k).value
                #print "Correct = %s" % dicChAttr['file']
                dicFiles['correct']=dicChAttr['file']
    return dicFiles

#---------------------------------------------------------------------------
def main():
    xmlBicLst=""
    curDate=strftime("%d.%m.%Y", localtime())
    sRevDate=strftime("%Y-%m-%d", localtime())
    #curDate="22.12.2011"
    #sRevDate="2008-10-29"
    saveDirDate=saveDir+curDate+"/"
    print "-----",curDate,"-----\n"
    xmlBicLst=ekGetFile(urlXmlDoc)
    bicData=ekParseXMLDoc(xmlBicLst, curDate)
    if bicData['correct'] == "":
        print "File does not exist on cbr server!"
        return 1
    print "Correct Bic file: %s" % bicData['correct']
    bicFileCorrect=ekGetFile(urlBicFile+bicData['correct'])
    try:
        os.mkdir(saveDirDate, 0777)
        #with open(saveDirDate+bicData['correct'], "wb") as f:
        f=open(saveDirDate+bicData['correct'], "wb")
        f.write(bicFileCorrect)
        print "File save to: %s%s" % (saveDirDate, bicData['correct'],)
        #os.rename()
        #os.chmod(,0644) 
    except OSError, error:
        print "ERROR: ", error
    else:
      f.close()
      print "\nDone ;)"
    return 0
#---------------------------------------------------------------------------
if __name__ == '__main__' :
  sys.exit( main() )

#----------------------------------------------------------------------------
#
