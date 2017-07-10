#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:
import cx_Oracle,sys,os
from dateutil import parser
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')
'''
客户端的NLS_LANG设置及编码转换

①在Oracle客户端向服务器端提交SQL语句时，Oracle客户端根据NLS_LANG和数据库字符集，对从应用程序接传送过来的字符串编码进行转换处理。
如果NLS_LANG与数据库字符集相同，不作转换，否则要转换成数据库字符集并传送到服务器。服务器在接收到字符串编码之后，对于普通的CHAR或
VARCHAR2类型，直接存储;对于NCHAR或NVARCHAR2类型，服务器端将其转换为国家字符集再存储。

①在Oracle客户端向服务器端提交SQL语句时，Oracle客户端根据NLS_LANG和数据库字符集，对从应用程序接传送过来的字符串编码进行转换处理。
如果NLS_LANG与数据库字符集相同，不作转换，否则要转换成数据库字符集并传送到服务器。服务器在接收到字符串编码之后，对于普通的CHAR或
VARCHAR2类型，直接存储;对于NCHAR或NVARCHAR2类型，服务器端将其转换为国家字符集再存储。

'''
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#连接ORCLE10G数据库
conn = cx_Oracle.connect('v5xuser/123456@192.168.0.235/oadb')
cursor = conn.cursor()
try:
    cursor.execute("SELECT * from ORG_UNIT where IS_ENABLE=1 AND IS_DELETED=0 and name not in ('集团','亿达信息','服务台')")
    result_unit = cursor.fetchall()
    # print  result_unit[0][2]
    row_unit = cursor.rowcount
    # print row_unit
    # for p in range(row_unit):
    #     for i in range(33):
    #         if   result_unit[p][i] is None:
    #
    #              print result_unit[p][i]
    #         # print type(result_unit[p][i])

    #查询出org_unit表来有多少行数据

    cursor.close()
    cursor = conn.cursor()

    #查询org_post表数据
    cursor.execute("SELECT * from ORG_POST ")
    result_post = cursor.fetchall()
    row_post = cursor.rowcount

    # 查询org_member表数据
    cursor.execute("SELECT *  from ORG_MEMBER where state=1 and is_enable=1 and IS_DELETED !=1 and name not like '%管理员' and name not like '%系统%' ")
    result_member = cursor.fetchall()
    row_member = cursor.rowcount
    # 查询org_level表数据
    cursor.execute("SELECT *  from ORG_LEVEL where status=1 and is_enable=1 ")
    result_level= cursor.fetchall()
    row_level = cursor.rowcount
    # print row_level
except ValueError:
    db.roolback
    print 'error'

#关闭游标和oracle数据库连接
cursor.close ()
conn.close ()

#连接mysql数据库参数字段
con = None
ip = '192.168.24.213'
user = 'root'
password ='xuanyuan'
dbname ='log_system'
port =3306
charset ='utf8'
db = MySQLdb.connect(host=ip,user=user,passwd=password,db=dbname,port=port,charset=charset)
cursor = db.cursor()

for j in range(row_unit):
    #org_unit 表数据写入
    sql_unit ="REPLACE INTO org_unit VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    %(result_unit[j][0],result_unit[j][1],result_unit[j][2],result_unit[j][3],result_unit[j][4],result_unit[j][5],result_unit[j][6],result_unit[j][7],result_unit[j][8],result_unit[j][9], \
      result_unit[j][10], result_unit[j][11], result_unit[j][12], result_unit[j][13], result_unit[j][14], result_unit[j][15], result_unit[j][16],result_unit[j][17], result_unit[j][18], result_unit[j][19], \
      result_unit[j][20], result_unit[j][21], result_unit[j][22], result_unit[j][23], result_unit[j][24], result_unit[j][25], result_unit[j][26], result_unit[j][27], result_unit[j][28], result_unit[j][29], \
      result_unit[j][30], result_unit[j][31], result_unit[j][32])
    sql_unit = sql_unit.replace('None','')
    print sql_unit

# 使用execute方法执行SQL语句
    try:
        cursor.execute('TRUNCATE TABLE org_unit')
        cursor.execute(sql_unit)

        # print  cursor.fetchall()[0][1]ex
        db.commit()
    except ValueError:

        db.roolback
        print 'error'

for j in range(row_post):
    #org_post表数据写入
    sql_post = "REPLACE INTO org_post VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
          % (result_post[j][0], result_post[j][1], result_post[j][2], result_post[j][3], result_post[j][4], result_post[j][5], result_post[j][6],
             result_post[j][7], result_post[j][8], result_post[j][9], \
             result_post[j][10], result_post[j][11])
    # print sql_post
    sql_post = sql_post.replace('None','')
    # 使用execute方法执行SQL语句
    try:
        cursor.execute('TRUNCATE TABLE org_post')
        cursor.execute(sql_post)

        # print  cursor.fetchall()[0][1]ex
        db.commit()
    except ValueError:

        db.roolback
        print 'error'

for j in range(row_member):
    # org_post表数据写入
    sql_member = "REPLACE INTO org_member VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'\
              ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'\
             ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" \
               % (result_member[j][0], result_member[j][1], result_member[j][2], result_member[j][3], result_member[j][4], result_member[j][5], result_member[j][6],
                  result_member[j][7], result_member[j][8], result_member[j][9],result_member[j][10], result_member[j][11],result_member[j][12], result_member[j][13], \
                  result_member[j][14], result_member[j][15], result_member[j][16], result_member[j][17], result_member[j][18], result_member[j][19], result_member[j][20], \
                  result_member[j][21], result_member[j][22], result_member[j][23], result_member[j][24], result_member[j][25], result_member[j][26], result_member[j][27] ,\
                  result_member[j][28], result_member[j][29], result_member[j][30], result_member[j][31], result_member[j][ 32], result_member[j][33], result_member[j][34], \
                  result_member[j][35], result_member[j][36], result_member[j][37], result_member[j][38], result_member[j][39], result_member[j][40], result_member[j][41] ,\
                  result_member[j][42], result_member[j][43], result_member[j][44], result_member[j][45], result_member[j][46], result_member[j][47], result_member[j][48] ,\
                  result_member[j][49], result_member[j][50], result_member[j][51], result_member[j][52], result_member[j][53], result_member[j][54], result_member[j][55], \
                  result_member[j][56]
                  )

    sql_member = sql_member.replace('None','')
    print sql_member
    # 使用execute方法执行SQL语句
    try:
        cursor.execute('TRUNCATE TABLE org_member')
        cursor.execute(sql_member)
        db.commit()
    except ValueError:

        db.roolback
        print 'error'

for j in range(row_level):
    # org_level 表数据写入
    sql_level = "REPLACE INTO org_level VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
               % (result_level[j][0], result_level[j][1], result_level[j][2], result_level[j][3], result_level[j][4],
                  result_level[j][5], result_level[j][6], result_level[j][7], result_level[j][8], result_level[j][9], \
                  result_level[j][10], result_level[j][11], result_level[j][12])
    sql_level = sql_level.replace('None', '')
    print sql_level

    # 使用execute方法执行SQL语句
    try:
        cursor.execute('TRUNCATE TABLE org_level')
        cursor.execute(sql_level)

        # print  cursor.fetchall()[0][1]ex
        db.commit()
    except ValueError:

        db.roolback
        print 'error'
#关闭游标和mysql数据库连接
cursor.close()
db.close()
