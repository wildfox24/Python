#!/usr/bin/env python
# -*- coding: utf8 -*-
#----------------------------------------------------------------------------
# Name:       vcxmlrpcs.py
# Version:    0.9.
# Purpose:    XML-RPC Server for verify certificates center.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    13.03.2008
# Updated:   14.03.2008
# Copyright:  (c) 2008 Klek
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
XML-RPC Server.
Verify clients certificates
'''
import web
Path="/home/www/htdocs/contact-sys/contents/"
def getFileContent(File):
    fin=open(Path+File, 'r')
    content=fin.read()
    fin.close()
    return content

class Content:
    #def __init__(self):
    #    pass

    def GET(self, QueryString):
        web.header('Content-Type', 'text/html; charset=windows-1251')
        if not QueryString: content='info.html'
        else: content=QueryString
        print "<body>"
        print "<meta http-equiv='Content-Type' content='text/html; charset=windows-1251'>\n";
        print "Превед, Орлы!<br>"
        print "Query_String = %s<br>" % (QueryString,)
        print getFileContent(content)
        print "</body>"

    def POST(self):
        web.header('Content-Type', 'text/html')
        #print response
        pass
web.webapi.internalerror = web.debugerror
urls = ('/(.*)', 'Content')
if __name__ == "__main__":  web.run(urls, globals(), web.reloader)
