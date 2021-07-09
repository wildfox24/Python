#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       selemium_ex1.py
# Version:    1.0.0
# Purpose:    
#
# Author:     Eugene Klepikov
# E-Mail:     klek07@ya.ru
#
# Created:    12.03.2020
# Updated:    12.03.2020
# Copyright:  (c) 2017 WildFox24
# Licence:    GPL
#----------------------------------------------------------------------------
##

from selenium import webdriver
 
driver = webdriver.Chrome()
driver.get("http://www.google.com")
 
elem = driver.find_element_by_name("q")
elem.send_keys("Hello WebDriver!")
elem.submit()
 
print(driver.title)
