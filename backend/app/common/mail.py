# -*- coding:utf-8 -*-
# Author:      LiuSha
import os
import smtplib
from email.header import make_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail:

    def __init__(self, username, password, smtp_server_addr, smtp_server_port):
        self.server = smtplib.SMTP_SSL(smtp_server_addr, smtp_server_port)
        self.server.login(username, password)
        self.sender = username.split('@')[0]

    def send_html(self, subject, receivers, content, files=None):
        #: files= ['name':'','path':path,]
        msg = MIMEMultipart()
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        msg['From'] = formataddr([self.sender, self.sender])
        msg['To'] = ",".join(receivers)
        msg['Subject'] = subject

        for file in files or []:
            filepath = file['path']

            if not os.path.exists(filepath):
                continue
            with open(filepath, "rb") as f:
                part = MIMEApplication(f.read(), Name=file["name"])

                hfilename = make_header([(file["name"], 'UTF-8')]).encode()
                part['Content-Disposition'] = f'attachment; filename="{hfilename}"'

            msg.attach(part)

        self.server.sendmail(self.sender, receivers, msg.as_string())
        self.server.quit()
        return True
