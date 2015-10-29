--Удаление зависих "страниц-детей"
--Перед этим необходимо авторизоваться и прописать PAGE_PRN_ID

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
remove_page = client.confluence2.getDescendents(authToken,str(PAGE_PRN_ID))

# таблица, в которой хранятся метаданные для проекта интерграции 
# PowerDesigner и Confluence - > "DEV_DB_STG.S_FILE_POWER_DESIGNER"
sql_remove = "SELECT PAGE_ID FROM DEV_DB_STG.S_FILE_POWER_DESIGNER where PAGE_ID is not null" # в качестве наглядного примера
connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
cursor.execute(sql_remove)
connect.commit()
table = cursor.fetchall()
for row in table:
    print(row[0])
    remove_page = row[0]
    client.confluence2.removePage(authToken,str(remove_page))
cursor.close
connect.close()

#Удаление метаданных в БД
sql = "DELETE FROM DEV_DB_STG.S_FILE_POWER_DESIGNER"
connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
cursor.execute(sql)
connect.commit()
cursor.close
connect.close()
