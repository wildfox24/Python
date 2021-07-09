#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       vcxmlrpcs.py
# Version:    0.9.1
# Purpose:    XML-RPC Server for verify certificates center.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    13.03.2008
# Updated:   18.03.2008
# Copyright:  (c) 2008 Klek
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
XML-RPC Server.
Verify clients certificates
'''
import web
import os
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
Path="c:/tmp/"
procVerifyEDS="c:\edmp\con_EDMP.exe -v -if"
def stroka(str):
    return str

def verifySigFile(Code, File):
    fout=open(Path+Code+'.xml', 'w')
    fout.write(File.encode('utf-8'))
    fout.close()
    #ret=subprocess.call([procVerifyEDS, argsVerifyEDS])
    ret=os.system('c:\edmp\con_EDMP.exe -v -ifc:\\tmp\\'+Code+'.xml'+' -ofc:\\tmp\data.txt')
    return ret

class XmlRpc:
    def __init__(self):
        self.dispatcher = SimpleXMLRPCDispatcher(False, 'utf-8')
        self.dispatcher.register_function(lambda x,y: x+y, 'add')
        self.dispatcher.register_function(stroka, 'str')
        self.dispatcher.register_function(verifySigFile, 'vrfDoc')
        self.dispatcher.register_introspection_functions()
    
    def GET(self):
        methods = self.dispatcher.system_listMethods()
        web.header('Content-Type', 'text/html')
        print "<body><h1>Error!</h1>"
        print "Method GET is not alowed for XMLRPC requests"
        print "List of available methods:"
        print "<ul>"
        for method in methods:
            sig = self.dispatcher.system_methodSignature(method)
            help =  self.dispatcher.system_methodHelp(method)
            print "<li><b>%s</b>: [%s] %s</li>" % (method, sig, help)
        print "</ul>"
        print "Be careful"
        print "</body>"

    def POST(self):
        response = self.dispatcher._marshaled_dispatch(web.webapi.data())
        web.header('Content-length', str(len(response)))
        print response

urls = ('/xml-rpc/', 'XmlRpc')
if __name__ == "__main__":
    web.run(urls, globals())
