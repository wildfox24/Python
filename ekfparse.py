#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       ekfparse.py
# Version:    0.2
# Purpose:    
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    06.11.2019
# Updated:    06.11.2019
# Copyright:  (c) 2019 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##
with open("ekfsync.dat", "rt") as f:
    for line in f:
		arg=(int(line.strip()))
		print(arg)
