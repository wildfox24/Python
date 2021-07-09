#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:       selemium_ex2.py
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
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome() #chromedriver.exe должен находиться в той же папке, что и этот скрипт!
driver.get("http://www.python.org") # Перейти по ссылке
assert "Python" in driver.title # Проерка есть ли в заголовке страницы слово Python
elem = driver.find_element_by_name("q") # найти элемент по id="q"
elem.clear() # очистить строку поиска перед печатанием
elem.send_keys("pycon") # отправляем текст в строку поиска 
elem.send_keys(Keys.RETURN) # имитируем нажатие клавиши Enter
assert "No results found." not in driver.page_source # Проверяем, что по-нашему запросу ничего не найдено.
driver.close() # закрываем браузер
