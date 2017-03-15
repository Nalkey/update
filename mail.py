# coding: utf-8

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Mail(object):
    def __init__(self):
        self.from_addr = 'yuanhao_wu@yeah.net'
        self.password = input('输入授权码')  # 这里指的是授权码，而非邮箱登录密码
        self.to_addr = '254138148@qq.com'
        self.smtp_server = 'smtp.yeah.net'

    # 收发人的名字格式一般为“user1 <xxx@xxx.com>”
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self, text):
        try:
            # 构建邮件
            msg = MIMEText(text, 'plain', 'utf-8')
            """msg = MIMEText('<html><body><h1>Hello</h1>' +
                '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
                '</body></html>', 'html', 'utf-8')"""
            msg['From'] = self._format_addr('浩南哥 <{}>'.format(self.from_addr))
            msg['To'] = self._format_addr('admin <{}>'.format(self.to_addr))
            msg['Subject'] = Header('来自洪兴帮的问候', 'utf-8').encode()
            # 发送邮件
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            # server.set_debuglevel(1)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            server.quit()
            return 'Mail is sent!'
        except smtplib.SMTPException as e:
            return e
