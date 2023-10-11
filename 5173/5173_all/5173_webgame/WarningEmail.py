# _*_coding:utf-8 _*_
# @Time　　 :2021/6/22/022   17:12
# @Author　 : Antipa
# @File　　 :WarningEmail.py
# @Theme    :PyCharm

import smtplib
from email.mime.text import MIMEText
from email.header import Header
def warning_email():
    from_addr='1569873132@qq.com'   #邮件发送账号
    qqCode='hyhnhdbfwveibacd'   #授权码（这个要填自己获取到的）
    to_addrs='getfunc@163.com'   #接收邮件账号
    smtp_server='smtp.qq.com'#固定写死
    smtp_port=465#固定端口

    #配置服务器
    stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
    stmp.login(from_addr,qqCode)

    #组装发送内容
    message = MIMEText('我是发送的内容', 'plain', 'utf-8')   #发送的内容
    message['From'] = Header("Python邮件预警系统", 'utf-8')   #发件人
    message['To'] = Header("管理员", 'utf-8')   #收件人
    subject = '【预警提醒】'
    message['Subject'] = Header(subject, 'utf-8')  #邮件标题

    try:
        stmp.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print ('邮件发送失败--' + str(e))
    else:
        print('【预警邮件】请处理异常')
