#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       vcxmlrpcs.py
# Version:    0.0.1
# Purpose:    XML-RPC Server for verify certificates center.
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
XML-RPC Server.
Verify clients certificates
'''
import cherrypy
class XmlRpc(cherrypy._cptools.XMLRPCController):
    def add(self, a, b):
        return a + b
    
    def str(self, str):
        return str

    def mult(self, a, b):
        return a* b

    add.exposed = True
    mult.exposed = True
    str.exposed = True

root = XmlRpc()
cherrypy.tree.mount(root, config={'/': {
     'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
}})

#cherrypy.server.ssl_certificate = "/etc/ssl/serts/server.crt"
#cherrypy.server.ssl_private_key = "/etc/ssl/private/server.key"
cherrypy.quickstart(root)
