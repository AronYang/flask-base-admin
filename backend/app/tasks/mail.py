# -*- coding:utf-8 -*-
# Author:      LiuSha
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.header import make_header
from app import current_app
from app.tasks import InvalidFnError, BaseTask


class Mail(BaseTask):

    def __init__(self, cron=False):
        self.cron = cron
        self.errmsg = None

        config = current_app.config["SRV"].get("MAIL", {})
        try:
            self.sender = config["USERNAME"]
            self.server = smtplib.SMTP_SSL(config["SMTP_SERVER_ADDR"], config["SMTP_SERVER_PORT"])
            self.server.login(config["USERNAME"], config["PASSWORD"])
        except Exception as err:
            self.errmsg = err

        super(Mail, self).__init__(cron=self.cron)

    def _generate_msg_to(self, receivers):
        users = self.run("wechat", "get_users")
        return [
            formataddr([
                users.get(receiver.split("@")[0], {}).get("name", receiver.split("@")[0]),
                receiver
            ])
            for receiver in receivers if "@" in receiver
        ]

    def send_html(self, subject, receivers, content, files=None):
        if self.errmsg:
            return self.update_task_log(self.server, self.failed)

        msg = MIMEMultipart()
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        msg['From'] = formataddr(["Mr.Lai", self.sender])
        msg['To'] = ",".join(self._generate_msg_to(receivers))
        msg['Subject'] = subject

        for file in files or []:
            filepath = os.path.join(current_app.config["STATIC_PATH"], file["path"].lstrip("/static/"))

            if not os.path.exists(filepath):
                continue
            with open(filepath, "rb") as f:
                part = MIMEApplication(f.read(), Name=file["name"])

                hfilename = make_header([(file["name"], 'UTF-8')]).encode()
                part['Content-Disposition'] = f'attachment; filename="{hfilename}"'

            msg.attach(part)

        try:
            self.server.sendmail(self.sender, receivers, msg.as_string())
            self.server.quit()
        except Exception as err:
            return self.update_task_log(str(err), self.failed)

        return self.update_task_log()
