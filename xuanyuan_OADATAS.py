#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:
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

# 将就的组织架构数据TRUNCATE
del_sql_unit = '''TRUNCATE TABLE tmp_umorg '''

# 将就的组织架构数据TRUNCATE
del_sql_umuser = '''TRUNCATE TABLE tmp_umuser '''

# 查询tmp_umuser中Loginid字段
tmp_loginid = '''SELECT USERNAME,LOGONID from tmp_umuser '''

# 最新组织架构数据
sql_unit = '''REPLACE into tmp_umorg(orgid,orgname,shortname,parentid,orgtype,CREATEDATE,PARENTIDS)
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
# 最新组织成员数据
sql_memer = '''replace into tmp_umuser(userid,username,position,position_type,createdate,password,email,mobile,PARENTIDS,orgid,orgname,status)

SELECT a.ID,a.`NAME`,b.name,c.name,a.create_time,

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
		when LENGTH(a.path)=16 then (SELECT CONCAT('670869647114347',',',a.id,',',b.id)from org_unit b where LENGTH(b.path)=12 and SUBSTR(a.path ,1 ,12)=b.path)
		when LENGTH(a.path)=20 then (SELECT CONCAT(a.id,',',b.id)from org_unit b where LENGTH(b.path)=16 and SUBSTR(a.path ,1 ,16)=b.path)
		when LENGTH(a.path)=24 then (SELECT CONCAT(a.id,',',b.id)from org_unit b where LENGTH(b.path)=20 and SUBSTR(a.path ,1 ,20)=b.path)
		else ''
		end as PARENTIDS,a.ORG_ACCOUNT_ID
		from org_unit a) m)  d on d.ID=a.ORG_DEPARTMENT_ID and d.ORG_ACCOUNT_ID=a.ORG_ACCOUNT_ID'''

# 字段为中文转换拼音实例
List_ID = []
py = pinyin.PinYin()
py.load_word()

# 使用execute方法执行SQL语句
try:
    # cursor.execute(del_sql_unit)
    # cursor.execute(del_sql_umuser)
    cursor.execute(sql_unit)
    cursor.execute(sql_memer)
    cursor.execute(tmp_loginid)
    loginid_sql = cursor.fetchall()
    loginid_row = cursor.rowcount
    for i in range(loginid_row):
        # loginid_sql[i][1] = py.hanzi2pinyin_split(string=loginid_sql[i][0], split="-").replace('-', '')
        # print loginid_sql[i][1]
        sql_pinyin = "update tmp_umuser set logonid = '%s' where username = '%s'" \
                     % (
                         py.hanzi2pinyin_split(string=loginid_sql[i][0], split="-").replace('-', ''), loginid_sql[i][0])
        print sql_pinyin
        cursor.execute(sql_pinyin)
    db.commit()

except ValueError:

    db.roolback
    print 'error'

# 同步tmp_umuser表到umuser表
syc_table_user = '''INSERT INTO umuser(USERID,USERNAME,position,position_type,LOGONID,`PASSWORD`,EMAIL,MOBILE,PARENTIDS,PARENTNAMES,
			ORGNAME,ORGID,SHOWORDER,CREATEDATE,PARENTTYPES,`STATUS`,del_flag) SELECT m.USERID,m.USERNAME,m.position,m.position_type,m.LOGONID,m.`PASSWORD`,m.EMAIL,m.MOBILE,m.PARENTIDS,m.PARENTNAMES,
			m.ORGNAME,m.ORGID,m.SHOWORDER,m.CREATEDATE,m.PARENTTYPES,m.`STATUS`,m.del_flag


	from (
		SELECT
			a.USERID,a.USERNAME,a.position,a.position_type,a.LOGONID,a.`PASSWORD`,a.EMAIL,a.MOBILE,a.PARENTIDS,a.PARENTNAMES,
			a.ORGNAME,a.ORGID,a.SHOWORDER,a.CREATEDATE,a.PARENTTYPES,a.`STATUS`,a.del_flag
		FROM
			tmp_umuser a
		WHERE
			a.USERID NOT IN (SELECT b.USERID FROM umuser b) 
	) m'''

# 同步tmp_umorg表到umorg表

syc_table_org = '''INSERT INTO umorg(orgid,orgname,parentid,orgtype,createdate,parentids,del_flag,leaf) 
SELECT m.orgid,m.orgname,m.parentid,m.orgtype,m.createdate,m.parentids,m.del_flag,m.leaf 
	from  (
		SELECT a.orgid,a.orgname,a.parentid,a.orgtype,a.createdate,a.parentids,a.del_flag,a.leaf from tmp_umorg a
		where a.orgid not in (SELECT b.orgid from umorg  b)
				) m 
'''
# 初始化人员权限表umuserrole
syc_table_roleright = '''INSERT INTO umuserrole(orgid,orgtype,roleids)
SELECT a.userid,'YG','40289481592f22bf01592f406ccb0044' 
from umuser a
where a.userid not in (SELECT b.orgid from umuserrole b )
'''
# OA组织架构表tmp_umorg与日志系统组织架构表umorg表对比，若日志系统系统有而OA没有者更新字段标志del_flg
update_umorg = '''UPDATE umorg  SET del_flag='1'
where ORGID not in (SELECT ORGID from tmp_umorg)'''
# 二次更新组织架构
update_umorg_two = '''UPDATE umorg a 
                            inner join tmp_umorg b on a.orgid=b.orgid
                            SET a.del_flag= b.del_flag,a.orgname=b.orgname,
                            a.parentid=b.parentid,a.parentids=b.parentids'''

# OA组织人员表tmp_umuser与日志系统组织人员表umuser对比，若日志系统系统有而OA没有者更新字段标志del_flg
update_umuser = '''UPDATE umuser  SET del_flag='1'
where userid not in (SELECT userid from tmp_umuser)'''
# 二次更新组织人员
update_umuser_two = '''UPDATE umuser a 
                                inner join tmp_umuser b on a.userid=b.userid
                                SET a.del_flag= b.del_flag,a.position=b.position,
                                a.position_type=b.position_type,a.email=b.email,
                                a.parentids=b.parentids,a.orgname=b.orgname,
                                a.orgid=b.orgid,a.logonid=SUBSTRING_INDEX(b.EMAIL,'@',1),a.USERNAME=b.USERNAME'''

try:
    cursor.execute(syc_table_user)
    cursor.execute(syc_table_org)
    cursor.execute(syc_table_roleright)
    cursor.execute(update_umorg)
    cursor.execute(update_umorg_two)
    cursor.execute(update_umuser)
    db.commit()

except ValueError:
    db.roolback
    print 'error'
# 关闭游标和mysql数据库连接
cursor.close()
db.close()

