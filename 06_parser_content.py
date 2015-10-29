#Пример замены контента в Confluence

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

sql_4_0 = "SELECT PAGE_ID FROM DEV_DB_STG.S_FILE_POWER_DESIGNER where FILE_EXT not in ('png','gif','txt','py','db','css','js') order by FILE_NAME, FILE_EXT"
print(sql_4_0)
connect4 = pyodbc.connect('DSN=TD')
cursor4 = connect4.cursor()
cursor4.execute(sql_4_0)
connect4.commit()
table_4 = cursor4.fetchall()
for row in table_4:
    print(row[0])
    replace_page = client.confluence2.getPage(authToken,str(row[0]))
    text = replace_page['content']
    sql_3_0 = "SELECT FULL_NAME, URL FROM DEV_DB_STG.S_FILE_POWER_DESIGNER where FILE_EXT not in ('txt','py','db') order by FILE_NAME, FILE_EXT"
    connect3 = pyodbc.connect('DSN=TD')
    cursor3 = connect3.cursor()
    cursor3.execute(sql_3_0)
    connect3.commit()
    table_3 = cursor3.fetchall()
    for row_3 in table_3:
        p = text.replace(str(row_3[0]),str(row_3[1]))
        #rep_from = '<td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Full2.htm">Previous</a></td></tr></table></td><td width=4></td>'
        #rep_to =  '<td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Full2.htm">Previous</a></td></tr></table></td><td width=4></td><td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Full LDM template_toc.html">Main</a></td></tr></table></td><td width=4></td>'
        #p = text.replace(rep_from, rep_to)
        #replace_page = client.confluence2.getPage(authToken,'885103840')
        #text = replace_page['content']
        #p = text.replace(str(row[1]),str(row[2]))
        replace_page['content']=p
        text = p
        text2 = replace_page['content']
        rep_from = '<td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Home_LightBlue.html">Home</a></td></tr></table></td>'
        rep_to =  '<td width=4></td><td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Home_LightBlue.html">Home</a></td></tr></table></td><td width=4></td><td><table class="NavGroup"><tr><td><a class="NavButton" href="https://it-portal.ru/display/DWH/Full LDM template_toc.html">Main</a></td></tr></table></td><td width=4></td>'
        p2 = text2.replace(rep_from, rep_to)
        replace_page['content']=p2
        text = p2
    client.confluence2.storePage(authToken,replace_page)
cursor3.close
connect3.close()
cursor4.close
connect4.close()
