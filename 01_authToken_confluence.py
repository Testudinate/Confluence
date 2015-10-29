-- Авторизация в Confluence

# -*- coding: utf-8 -*-
from __future__ import with_statement
#import sys, string,  re, os
#import pyodbc
import xmlrpc.client #для версии python 3.4.*
#import codecs

URL ='' #адрес WIKI -> default
username = '' #ваш логин
pwd = '' #ваш пароль
client = xmlrpc.client.ServerProxy(URL+'/rpc/xmlrpc') #API.XMLRPC
authToken = client.confluence2.login(username,pwd)  #API.авторизация
