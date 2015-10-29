#Добавление вложений в confluence, а также обновление метаданных

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

sql_5_0 = "SELECT FILE_PATH,PAGE_PRN_ID, FILE_EXT,FULL_NAME FROM DEV_DB_STG.S_FILE_POWER_DESIGNER where FILE_EXT in ('png','gif','css','js') order by FILE_NAME, FILE_EXT"
print(sql_5_0)
connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
cursor.execute(sql_5_0)
connect.commit()
table_5 = cursor.fetchall()
for row in table_5:
    print(row[0],row[2])
    if row[2] == 'gif':
        contentType = 'image/gif'
    elif row[2] == 'png':
        contentType = 'image/png'
    elif row[2] == 'css':
        contentType = 'text/css'
    elif row[2] == 'js':
        contentType = 'application/x-javascript'
    path = row[0]
    f = open(path,'rb')
    data = f.read()
    filename = row[3]
    page_id = row[1]
    page = client.confluence2.getPage(authToken, str(page_id))
    client.confluence2.removeAttachment(authToken, str(page_id),str(filename))
    print('file remove')
    if page is None:
        exit("Could not find page " + spacekey + ":" + str(page['title']))
    attachment = {}
    attachment['fileName'] =os.path.basename(filename)
    attachment['contentType'] = contentType
    print(page['id'])
    client.confluence2.addAttachment(authToken, page['id'], attachment, xmlrpc.client.Binary(data))
f.close
cursor.close
connect.close()
#-----------------------------------------------------------------------------------------------------
page_attachment = '885102819'
text = client.confluence2.getAttachments(authToken,page_attachment)
connect = pyodbc.connect('DSN=TD')
cursor = connect.cursor()
for i in range(len(text)):
    sql_6_1 = "UPDATE DEV_DB_STG.S_FILE_POWER_DESIGNER set URL ='"+str(text[i]['url']) + u"' where FULL_NAME = '" + str(text[i]['fileName'])+u"';"
    cursor.execute(sql_6_1)
    connect.commit()
    i = i + 1
cursor.close
connect.close()
