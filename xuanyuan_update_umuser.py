#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2018-06-28
# from dateutil import parser
import cx_Oracle, sys, os
import MySQLdb
import pinyin

reload(sys)
sys.setdefaultencoding('utf8')
'''
客户端的NLS_LANG设置及编码转换

①在Oracle客户端向服务器端提交SQL语句时，Oracle客户端根据NLS_LANG和数据库字符集，对从应用程序接传送过来的字符串编码进行转换处理。
如果NLS_LANG与数据库字符集相同，不作转换，否则要转换成数据库字符集并传送到服务器。服务器在接收到字符串编码之后，对于普通的CHAR或
VARCHAR2类型，直接存储;对于NCHAR或NVARCHAR2类型，服务器端将其转换为国家字符集再存储。
'''
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# 连接mysql数据库参数字段
con = None
ip = '192.168.29.132'
user = 'root'
password = 'xuanyuan@123'
dbname = 'log_system'
port = 3306
charset = 'utf8'
db = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, port=port, charset=charset)
cursor = db.cursor()

# 二次更新组织人员
update_umuser_two = '''UPDATE umuser a 
                                inner join tmp_umuser b on a.userid=b.userid
                                SET a.del_flag= b.del_flag,a.position=b.position,
                                a.position_type=b.position_type,a.email=b.email,
                                a.parentids=b.parentids,a.orgname=b.orgname,
                                a.orgid=b.orgid,a.logonid=case when  a.LOGONID='' then b.LOGONID ELSE SUBSTRING_INDEX(b.EMAIL,'@',1) end '''

try:

    cursor.execute(update_umuser_two)

    db.commit()

except ValueError:
    db.roolback
    print 'error'
# 关闭游标和mysql数据库连接
cursor.close()
db.close()

