#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       webpyxmlrpc.py
# Version:    1.0.0
# Purpose:    WebPy XML-RPC Server.
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@gmail.com
#
# Created:    13.03.2008
# Updated:   13.03.2008
# Copyright:  (c) 2008 Klek
# Licence:    GPL
#----------------------------------------------------------------------------
##
'''
WebPy XML-RPC Server.
'''
import web
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
dispatcher = SimpleXMLRPCDispatcher(None, None)

def stroka(str):
    return str
    
class xmlrpc:
    def __init__(self):
        global dispatcher
        dispatcher.register_function(lambda x,y: x+y, 'add')
        dispatcher.register_function(stroka, 'str')
    
    def GET(self):
        global dispatcher
        methods = dispatcher.system_listMethods()
        web.header('Content-Type', 'text/html')
        print "<body><h1>Error!</h1>"
        print "Method GET is not alowed for XMLRPC requests"
        print "List of available methods:"
        print "<ul>"
        for method in methods:
            sig = dispatcher.system_methodSignature(method)
            help =  dispatcher.system_methodHelp(method)
            print "<li><b>%s</b>: [%s] %s</li>" % (method, sig, help)
        print "</ul>"
        print "Be careful"
        print "</body>"

    def POST(self):
        global dispatcher
        response = dispatcher._marshaled_dispatch(web.webapi.data())
        web.header('Content-length', str(len(response)))
        print response
