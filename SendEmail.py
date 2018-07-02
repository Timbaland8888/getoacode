#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:20180629
import smtplib
import cx_Oracle,sys,os
# from dateutil import parser
import MySQLdb
from email.mime.text import MIMEText
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
ip = '192.168.29.132'
user = 'root'
password ='xuanyuan@123'
dbname ='log_system'
port = 3321
charset ='utf8'
db = MySQLdb.connect(host=ip,user=user,passwd=password,db=dbname,port=port,charset=charset)
cursor = db.cursor()
umuser_query ='''SELECT username,COALESCE(orgname,'---') as org,COALESCE(position,'---'),COALESCE(position_type,'---'),'---' as email from tmp_umuser 
where orgname not like '%职赢未来%' and  del_flag='0' and email not like '%@%' or email is null  '''
try:
     cursor.execute(umuser_query)
     result = cursor.fetchall()
     result_row = cursor.rowcount
     db.commit()

except ValueError:
    db.roolback
    print 'error'
#关闭游标和mysql数据库连接
cursor.close()
db.close()
mail_msg =''
name_info = ''
org_info = ''
position_info =''
position_type_info =''
mail_msg = """
<html>
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
table.gridtable caption
{padding:10px 0px;
font-size:20px;
color:#c00;
} 
</style>
<body>
<div> 
Dear 程林： 
</div><br> 
<div style="margin-left:auto;"> 
&nbsp;&nbsp;&nbsp;由于日志系统用到了在职人员职位和邮箱信息，以下<font color='black'><b>"人员信息表"</b></font>共<font color='red'><b><strong>%d</strong></b></font>人信息不完整，<br>&nbsp;&nbsp;&nbsp;请帮忙登入OA系统补录完整，谢谢！
</div><br> 
<table class="gridtable" >
    <caption>人员信息表</caption>
<tr>
	<th>姓名</th><th>部门</th><th>职位类型</th><th>职位</th><th>邮箱</th>
</tr>
"""%(result_row)
html_end = '''</table><font color='red'><b>备注:</b></font>"---"代表缺失
</div><br>
<div> 
<img src="https://gss0.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/cf1b9d16fdfaaf5175e3b407865494eef01f7a01.jpg" > 
</div> 
<div> 
<p>轩辕项目信息管理系统</p> 
<p>广东轩辕网络科技股份有限公司</p> 
<p>总部：广州市天河区国家软件产业基地高普路1033号B座8层   邮编：510663</p> 
<p>网址：http://www.xuanyuan.com.cn</p> 
<p>总机：020-3730 5423     传真：020-8528 5329</p> 
</div> 
</body>
</html>'''

for i in range(result_row):

    mail_msg += '<tr><td>'+result[i][0]
    mail_msg += '</td><td>'+result[i][1]
    mail_msg += '</td><td>'+result[i][2]
    mail_msg += '</td><td>'+result[i][3]
    mail_msg += '</td><td>'+result[i][4]+'</td>'
mail_msg += html_end
print mail_msg
# 收件人列表
# mail_namelist = ['yanshanghua@xuanyuan.com.cn','chenglin@xuanyuan.com.cn']
mail_namelist =["422033564@qq.com",'leixiangling@xuanyuan.com.cn']
# 发送方信息
mail_user = "rzglxt@xuanyuan.com.cn"
#口令
# mail_pass = "rlixtgnujleocagi"
mail_pass = "1234qwer"
#发送邮件
#title：标题
#conen：内容
def send_qq_email(title,conen):
    try:
        msg = MIMEText(str(conen),'html','utf-8')
        #设置标题
        msg["Subject"] = title
        # 发件邮箱
        msg["From"] = mail_user
        #收件邮箱
        msg["To"] = ";".join(mail_namelist)
        # 设置服务器、端口
        # s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s = smtplib.SMTP_SSL("mail.xuanyuan.com.cn", 465)
        #登录邮箱
        s.login(mail_user, mail_pass)
        # 发送邮件
        s.sendmail(mail_user, mail_namelist, msg.as_string())
        s.quit()
        print("邮件发送成功!")
        return True
    except smtplib.SMTPException:
        print("邮件发送失败！")
        return False

if __name__ == '__main__':
    if result_row > 0:
        send_qq_email("没有邮箱人员",mail_msg)
    else:
        print '没有不完整人员'