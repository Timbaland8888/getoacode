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

#连接mysql数据库参数字段
con = None
ip = '58.67.220.228'
user = 'root'
password ='xuanyuan@123'
dbname ='log_system'
port = 3321
charset ='utf8'
db = MySQLdb.connect(host=ip,user=user,passwd=password,db=dbname,port=port,charset=charset)
cursor = db.cursor()

#将就的组织架构数据TRUNCATE
del_sql_unit = '''TRUNCATE TABLE tmp_umorg '''

#将就的组织架构数据TRUNCATE
del_sql_umuser= '''TRUNCATE TABLE tmp_umuser '''

#最新组织架构数据
sql_unit ='''REPLACE into tmp_umorg(orgid,orgname,shortname,parentid,orgtype,CREATEDATE,PARENTIDS)
	SELECT k.id,k.name,k.short_name,k.PARENTID,k.ORGTYPE,k.create_time, 
					case when LENGTH(k.path)=24 then (SELECT CONCAT(k.PARENTIDS,',',b.id) from org_unit b
								                        where LENGTH(b.path)=16 and SUBSTR(k.path ,1 ,16)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
					else  k.PARENTIDS end as PARENTIDS
	from (select m.id,m.name,m.short_name ,m.PARENTID,m.ORGTYPE,m.create_time,m.path,
				  case when LENGTH(m.path)=20 then (SELECT CONCAT(m.PARENTIDS,',',b.id) from org_unit b
													   where LENGTH(b.path)=12 and SUBSTR(m.path ,1 ,12)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
					   when LENGTH(m.path)=24 then (SELECT CONCAT(m.PARENTIDS,',',b.id)from org_unit b
													  where LENGTH(b.path)=12 and SUBSTR(m.path ,1 ,12)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
				  else  m.PARENTIDS end as PARENTIDS from
										(SELECT a.id,a.name,a.short_name,a.path,
										case when LENGTH(a.path)=12  then (SELECT id from org_unit where path='00000001' and IS_ENABLE=1 AND IS_DELETED=0)
										when LENGTH(a.path)=16 then (SELECT b.id from org_unit b where LENGTH(b.path)=12 and SUBSTR(a.path ,1 ,12)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
										when LENGTH(a.path)=20 then (SELECT b.id from org_unit b where LENGTH(b.path)=16 and SUBSTR(a.path ,1 ,16)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
										when LENGTH(a.path)=24 then (SELECT b.id from org_unit b where LENGTH(b.path)=20 and SUBSTR(a.path ,1 ,20)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
										else ''
										end as PARENTID ,
										'GS' as ORGTYPE,
										a.create_time,
										case when LENGTH(a.path)=8 then (SELECT id from org_unit where path='00000001' and IS_ENABLE=1 AND IS_DELETED=0)
										when LENGTH(a.path)=12 then (SELECT id from org_unit where path='00000001' and IS_ENABLE=1 AND IS_DELETED=0)
										when LENGTH(a.path)=16 then (SELECT CONCAT('670869647114347',',',b.id)from org_unit b where LENGTH(b.path)=12 and SUBSTR(a.path ,1 ,12)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0)
										when LENGTH(a.path)=20 then (SELECT CONCAT('670869647114347',',',b.id)from org_unit b
																	   where LENGTH(b.path)=16 and SUBSTR(a.path ,1 ,16)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0
																								)
										when LENGTH(a.path)=24 then (SELECT CONCAT('670869647114347',',',b.id)from org_unit b
																	   where LENGTH(b.path)=20 and SUBSTR(a.path ,1 ,20)=b.path and b.IS_ENABLE=1 AND b.IS_DELETED=0
																								)
										else ''
										end as PARENTIDS
										from org_unit a where a.IS_ENABLE=1 AND a.IS_DELETED=0) m)k'''
#最新组织成员数据
sql_memer = '''replace into tmp_umuser(userid,username,position,position_type,LOGONID,password,email,mobile,PARENTIDS,orgid,orgname,status)

SELECT a.ID,a.`NAME`,b.name,c.name,
				to_pinyin(a.`NAME`) as login_id,
			 'e10adc3949ba59abbe56e057f20f883e' as pwd,
			 a.EXT_ATTR_2 as email,a.EXT_ATTR_1 as moblie,
			 d.parentids,a.ORG_DEPARTMENT_ID,d.name,a.status
from org_member a
INNER JOIN org_level b on b.id=a.org_level_id
INNER JOIN  org_post c on c.id=a.org_post_id
INNER JOIN (select m.id,m.name,m.short_name ,m.PARENTID,m.ORGTYPE,m.create_time,
									case when LENGTH(m.path)=20 then (SELECT CONCAT('670869647114347',',',b.id,',',m.PARENTIDS)from org_unit b
																 where LENGTH(b.path)=12 and SUBSTR(m.path ,1 ,12)=b.path)
									     when LENGTH(m.path)=24 then (SELECT CONCAT('670869647114347',',',b.id,',',m.PARENTIDS)from org_unit b
																 where LENGTH(b.path)=12 and SUBSTR(m.path ,1 ,12)=b.path)
									else  m.PARENTIDS end as PARENTIDS ,m.ORG_ACCOUNT_ID from
		(SELECT a.id,a.name,a.short_name,a.path,
		case when LENGTH(a.path)=12  then (SELECT id from org_unit where path='00000001')
		when LENGTH(a.path)=16 then (SELECT b.id from org_unit b where LENGTH(b.path)=12 and SUBSTR(a.path ,1 ,12)=b.path)
		when LENGTH(a.path)=20 then (SELECT b.id from org_unit b where LENGTH(b.path)=16 and SUBSTR(a.path ,1 ,16)=b.path)
		when LENGTH(a.path)=24 then (SELECT b.id from org_unit b where LENGTH(b.path)=20 and SUBSTR(a.path ,1 ,20)=b.path)
		else ''
		end as PARENTID ,
		'GS' as ORGTYPE,
		a.create_time,
		case when LENGTH(a.path)=8 then (SELECT id from org_unit where path='00000001')
		when LENGTH(a.path)=12 then (SELECT CONCAT(a.id,',',b.id) from org_unit b where LENGTH(b.path)=8 and SUBSTR(a.path ,1 ,8)=b.path)
		when LENGTH(a.path)=16 then (SELECT CONCAT(a.id,',',b.id)from org_unit b where LENGTH(b.path)=12 and SUBSTR(a.path ,1 ,12)=b.path)
		when LENGTH(a.path)=20 then (SELECT CONCAT(a.id,',',b.id)from org_unit b where LENGTH(b.path)=16 and SUBSTR(a.path ,1 ,16)=b.path)
		when LENGTH(a.path)=24 then (SELECT CONCAT(a.id,',',b.id)from org_unit b where LENGTH(b.path)=20 and SUBSTR(a.path ,1 ,20)=b.path)
		else ''
		end as PARENTIDS,a.ORG_ACCOUNT_ID
		from org_unit a) m)  d on d.ID=a.ORG_DEPARTMENT_ID and d.ORG_ACCOUNT_ID=a.ORG_ACCOUNT_ID'''

# 使用execute方法执行SQL语句
try:
        cursor.execute(del_sql_unit)
        cursor.execute(del_sql_umuser)
        cursor.execute(sql_unit)
        cursor.execute(sql_memer)
        db.commit()
except ValueError:

        db.roolback
        print 'error'


#关闭游标和mysql数据库连接
cursor.close()
db.close()
