from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

subject = 'May the Force Be With You!'
sendfrom = '422033564@qq.com'
sendto = '422033564@qq.com'
copyto = '422033564@qq.com'

msg = MIMEMultipart('related')
msg['Subject'] = subject
msg['From'] = sendfrom
msg['To'] = sendto
msg['CC'] = copyto
mail_user = "422033564@qq.com"

mail_pass = "rlixtgnujleocagi"

content = MIMEText('<html><body><img src="cid:digglife" alt="digglife"></body></html>')
msg.attach(content, 'html')


fp = open('/tim/Local_OA/fox.jpg', 'rb')
img = MIMEImage(fp.read())
img.add_header('Content-ID', 'digglife')
msg.attach(img)

s = smtplib.SMTP_SSL("smtp.qq.com", 465)

s.login(mail_user, mail_pass)

s.sendmail(sendfrom, [sendto, copyto], msg.as_string())
s.quit()

