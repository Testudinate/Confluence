#Создание таблиц в Confluence и обновление метаданных в БД

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

new_page = dict()

sql_2_0 = "SELECT FULL_NAME , PAGE_PRN_ID FROM DEV_DB_STG.S_FILE_POWER_DESIGNER where FILE_EXT not in ('png','gif','txt','py','db','css','js') order by FILE_NAME, FILE_EXT"
print(sql_2_0)
connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
cursor.execute(sql_2_0)
connect.commit()
table_2 = cursor.fetchall()
for row in table_2:
    print(row[0],row[1])
    sql = "SELECT FULL_NAME FROM DEV_DB_STG.S_FILE_POWER_DESIGNER  where FILE_EXT not in ('png','gif','txt','py','db') "
    connect = pyodbc.connect('DSN=TD')
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()
    table = cursor.fetchall()
    for row_in in table:
        print(row_in[0])
        #можно переписать этот код! 1\2
        if row_in[0]=='Full LDM template.html' and row[0]==row_in[0]:
            path = 'C:\PD\\' #можно переписать 
            path = path + row[0]
            f = codecs.open(str(path),'r','utf-8')
            words = f.read()
            new_page['title']=row[0]   
            new_page['content']=u'<ac:macro ac:name="html"><ac:plain-text-body><![CDATA[' + str(words) + u']]></ac:plain-text-body></ac:macro>'
            new_page['parentId'] =PAGE_PRN_ID
            new_page['space'] ='DWH'
            page = client.confluence2.storePage(authToken,new_page)
            page_get = page['id']
            info = client.confluence2.getPage(authToken,page_get)
            sql_2_1 = "UPDATE DEV_DB_STG.S_FILE_POWER_DESIGNER set PAGE_ID = " + info['id']+u" , PAGE_TITLE = '" + info['title'] + u"', URL ='"+info['url'] + u"' where PAGE_PRN_ID = "+str(row[1])+u" and FULL_NAME = '" + str(row[0])+u"';"
            cursor.execute(sql_2_1)
            connect.commit()
            f.close
        elif row[0]==row_in[0]:
            path = 'C:\PD\Full LDM template_files\\' #можно переписать 
            path = path + row[0]
            f = codecs.open(str(path),'r','utf-8')
            words = f.read()
            
            new_page['title']=row[0]   
            new_page['content']=u'<ac:macro ac:name="html"><ac:plain-text-body><![CDATA[' + str(words) + u']]></ac:plain-text-body></ac:macro>'
            new_page['parentId'] =PAGE_PRN_ID
            new_page['space'] ='DWH'
            page = client.confluence2.storePage(authToken,new_page)
            page_get = page['id']
            info = client.confluence2.getPage(authToken,page_get)
            sql_2_1 = "UPDATE DEV_DB_STG.S_FILE_POWER_DESIGNER set PAGE_ID = " + info['id']+u" , PAGE_TITLE = '" + info['title'] + u"', URL ='"+info['url'] + u"' where PAGE_PRN_ID = "+str(row[1])+u" and FULL_NAME = '" + str(row[0])+u"';"
            cursor.execute(sql_2_1)
            connect.commit()
            f.close
cursor.close
connect.close()
