#Получение списка файлов для загрузки в Confluence. Сохранение метаданных в БД

# -*- coding: utf-8 -*-
from __future__ import with_statement
import sys, string,  re, os
import pyodbc
import xmlrpc.client
import codecs

URL ='' 
username = '' #логин
pwd = '' #пароль
client = xmlrpc.client.ServerProxy(URL+'/rpc/xmlrpc') #API.XMLRPC
authToken = client.confluence2.login(username,pwd)  #API.авторизация

PAGE_PRN_ID = '885102819'

connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
for top, dirs, files in os.walk('C:\PD'):
    for nm in files:
        text = (os.path.join(top,nm))
        t = os.path.split(text)
        full_name = t[1]
        t = os.path.splitext(t[1])
        sql_1 = ''
        print(t[1])
        sql_0 = 'INSERT INTO DEV_DB_STG.S_FILE_POWER_DESIGNER (FILE_NAME,FILE_EXT,FULL_NAME,PAGE_PRN_ID,FILE_PATH) VALUES('
        sql_1 = sql_0 + u"'"+ t[0]+u"','"+t[1].split('.')[1] + u"','"+ full_name +u"','"+ PAGE_PRN_ID +u"','" + text + u"')"
        print(sql_1)
        cursor.execute(sql_1)
connect.commit()
cursor.close
connect.close()
