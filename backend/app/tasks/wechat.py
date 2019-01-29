# -*- coding:utf-8 -*-
# Author:    Aaron
# 企业微信接口

import string

from aip import AipSpeech
from pypinyin import lazy_pinyin
from passlib.hash import ldap_salted_sha1 as lsa

from random import choice, choices
from copy import deepcopy
from datetime import datetime
from app import current_app, cache
from app.common.log import Log
from app.common.http import request
from app.tasks import InvalidConfigError, InvalidFnError, BaseTask
from app.common.ldap import LdapClient
from app.models.issue_report import IssueReport
from app.models.workorder_ticket import WorkorderTicket


#: Cache Type -> str
TOKEN_CACHE_KEY = "WECHAT_ACCESS_TOKEN"
USER_LIST_CACHE_KEY = "WECHAT_USER_LIST"

ONDUTY_CACHE_KEY = "WECHAT_ONDUTY"

USER_ID = 17032302

#: ALL
DEPARTMENT_ID_LIST = [1]

#: API SENDER 任务的地址， 暂时写死
API_SENDER_SMS_ENDPOINT = "http://218.17.194.101:18081/api/sendsms"

#: Smart-DevOps - 16816722483962180943
#: 阿里云-审计日志 - 17326473666785178995
#: 测试环境-告警通知 - 10547430327685739893
#: 生产环境-告警通知 - 17763885780593538422
#: 测试环境-问题处理 - 16424064891450815878
#: 东南亚生产-告警通知 - 15072422056597259556
#: 【绿创办公室】IT 问题沟通与处理 - 13564560603047281058
#: 【任务调度】调用通知 - 12681855079393658054
#: 【阿里大厦】- IT 问题沟通与处理 - 11733284404567757764
#: 客服系统-问题沟通与处理 - 15549522138810831813
#: 数据库-告警通知 - 9773655616708174990
#: 【生产环境】问题沟通与处理 - 12481444892664686010


class Wechat(BaseTask):

    def __init__(self, config, cron=False):
        if not config:
            raise InvalidConfigError("invalid wechat config")

        self.cron = cron
        super(Wechat, self).__init__(cron=self.cron)

        self.corp_id = config["CORP_ID"]
        self.secret = config["SECRET"]
        self.agent_id = config["AGENT_ID"]
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin"
        self.logger = Log(f'tasks_{self.__class__.__name__.lower()}', cmdlevel="DEBUG" if current_app.debug else "INFO")

    @classmethod
    def email_to_username(cls, email):
        """
        :param email: str
        :return: str
        """
        arr = email.lower().split("@")
        if len(arr) > 1:
            return arr[0]

        return email

    @classmethod
    def user_adjust(cls, user):
        """
        Adjust user data
        :param user: dict
        :return: dict
        """

        return {
            "userid": user["userid"], "name": user["name"], "position": user["position"],
            "mobile": user["mobile"], "gender": user["gender"], "email": user["email"].lower(),
            "status": user["status"],  "avatar": user["avatar"], "department": user["department"],
            "username": cls.email_to_username(user["email"])}

    def refresh_token(self):
        """
        :return: access_token <str>
        """
        token_url = f"{self.base_url}/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"

        res = request("GET", token_url).json()
        self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

        if res["errcode"] == 0:
            cache.set(TOKEN_CACHE_KEY, res.get("access_token"), timeout=res.get("expires_in"))

        return res.get("access_token")

    def refresh_users(self):
        """
        :return: users <list>
        """
        self.get_user()

        users = {}
        for department_id in DEPARTMENT_ID_LIST:
            users_url = (
                f"{self.base_url}/user/list?access_token={self.get_token()}&"
                f"department_id={department_id}&fetch_child=1"
            )

            res = request("GET", users_url).json()
            self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

            if res["errcode"] == 0:
                users = {
                    **users,
                    **{user["userid"]: self.user_adjust(user) for user in res["userlist"]},
                    **{self.email_to_username(user["email"]): self.user_adjust(user) for user in res["userlist"]}
                }

                users["admin"] = deepcopy(users["freedie.liu"])
                users["admin"].pop("department")

                cache.set(USER_LIST_CACHE_KEY, users, timeout=600)

        return cache.get(USER_LIST_CACHE_KEY) or {}

    def refresh_departments(self):
        users_url = (
            f"{self.base_url}/department/list?access_token={self.get_token()}&"
            f"id=1"
        )

        res = request("GET", users_url).json()
        self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

        #: {i["id"]: {"name": i["name"], "parentid": i["parentid"]} for i in d}
        return res["department"]

    def get_token(self):
        access_token = cache.get(TOKEN_CACHE_KEY)
        if not access_token:
            access_token = self.refresh_token()

        return access_token

    def get_users(self):
        """
        :return: user list <list>
        """
        users = cache.get(USER_LIST_CACHE_KEY)

        if not isinstance(users, dict) or not users:
            users = self.refresh_users()

        return users

    def convert_to_touser(self, user_list):
        """
        convert user_list to touser
        :param: user_list <list>
        :return: touser <str>
        """
        users = self.get_users()

        return "|".join([
            users[user.lower() if isinstance(user, str) else user].get("userid")
            for user in user_list

            if isinstance(users.get(user.lower()), dict) and user.lower() in users
        ])

    def get_user(self, user_id=USER_ID):
        """
        :param user_id: user id <int>
        :return: user detail
        """
        user_url = f"{self.base_url}/user/get?access_token={self.get_token()}&userid={user_id}"

        res = request("GET", user_url).json()
        self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

        if res["errcode"] == 40014:
            self.refresh_token()

        if res["errcode"] != 0:
            return {}

        return self.user_adjust(res)

    def send(self, user_list=None, content=None):
        """
        Content item supports inline a tags. When item is int, it will turn into string
        :param user_list: <list>
        :param content: <str>
        :return: success or error msg
        """
        self.get_user()
        send_url = f"{self.base_url}/message/send?access_token={self.get_token()}"

        if not isinstance(user_list, list) or not isinstance(content, str):
            return "invalid user_id list or content list"

        playload = {
            "msgtype": "text",
            "touser": self.convert_to_touser(user_list),
            "agentid": self.agent_id,
            "text": {"content": content}
        }

        res = request("POST", send_url, json=playload).json()
        self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

        if res["errcode"] != 0:
            if not self.cron:
                self.update_task_log(res["errmsg"], status="failed")
            return res["errmsg"]

        return self.update_task_log()

    def push(self, chat_id=None, content=None):
        """
        Content item supports inline a tags. When item is int, it will turn into string
        :param chat_id: <str>
        :param content: <str>
        :return: success or error msg
        """
        self.get_user()
        push_url = f"{self.base_url}/appchat/send?access_token={self.get_token()}"

        playload = {
            "msgtype": "text",
            "chatid": chat_id,
            "safe": 0,
            "text": {"content": content}
        }

        res = request("POST", push_url, json=playload).json()
        self.logger.info(f"request errcode:{res['errcode']} | errmsg:{res['errmsg']}")

        if res["errcode"] != 0:
            if not self.cron:
                self.update_task_log(res["errmsg"], status="failed")
            return res["errmsg"]

        return self.update_task_log()

    def send_publish_report(self, message):
        users = self.get_users()
        user = users.get(message["from"])

        contents = []
        tickets = WorkorderTicket.get_by_current_day()

        for ticket in tickets:
            if ticket.status == 1:
                status = "审核中"
            elif ticket.status == 3:
                status = "接单处理中"
            elif ticket.status == 5:
                status = "结果验证中"
            elif ticket.status == 7:
                status = "验证无误待关闭"
            elif ticket.status == 9:
                status = "被拒绝"
            elif ticket.status == 11:
                status = "已关闭"
            elif ticket.status == 13:
                status = "任务运行中"

            contents.append(
                f'{ticket.title} - {ticket.created_by} - {status}'
            )

        self.run("wechat", "send", user_list=[user["username"]], content='\n'.join(contents))

    def create_ldap_account(self, message):
        try:
            ldap = LdapClient(current_app.config["SRV"].get("LDAP", {}))
        except (TypeError, KeyError) as err:
            return self.update_task_log(result=str(err), status=self.failed)

        users = self.get_users()
        user = users.get(message["from"])
        user["username"] = user["username"].lower()

        password = ''.join(choices(string.ascii_uppercase + string.digits, k=12))
        reset_link = 'https://open.work.weixin.qq.com/wwopen/mpnews?' \
                     'mixuin=shVSBgAABwCLHi64AAAUAA&' \
                     'mfid=WW0321-v51MHQAABwDf1_RQrCcQCw_L6lg2b&' \
                     'idx=0&sn=67b6a0162f2b0c6de66e50f910fdcc6f&version=2.4.16.2041&platform=mac'

        if ldap.get_user(user["username"]):
            self.send([user["username"]], f"<a href='{reset_link}'>您在平台已有账号，点击本消息以查看如何修改密码</a>")
            return self.update_task_log()

        ldap.add_user({
            'cn': user["username"],
            'uid': user["username"],
            'uidNumber': ldap.get_available_uid(gid=15020),
            'sn': user["username"].split(".")[0],
            'givenName': user["username"].split(".")[1],
            'gidNumber': 15020,

            'homeDirectory': f'/home/{user["username"]}',
            'loginShell': '/sbin/nologin',
            'pwdAttribute': 'userPassword',
            'pwdMaxFailure': '5',
            'shadowMax': '99999',
            'shadowMin': '0',
            'shadowWarning': '7',

            'userPassword': lsa.hash(password.encode()),
            'mail': user["email"] or "undefined",
            'telephoneNumber': user["mobile"] or "undefined",
            'description': "企业微信"
        })

        self.run("wechat", "send", user_list=[user["username"]], content=(
            f'平台账户创建成功:\n'
            f'账号: {user["username"]}\n'
            f'密码: {password}\n'
            f'手机号码: {user["mobile"]}\n'
            f'邮箱地址: {user["email"]}\n\n'
            f'用途: 运维支撑平台、Git、堡垒机等服务使用。'
        ))

        self.run("wechat", "send", user_list=[user["username"]], content=(
            f'<a href="{reset_link}">您也可通过点击本消息以查看如何重置密码</a>'
        ))

        return self.update_task_log()

    def write_to_ldap(self):
        try:
            ldap = LdapClient(current_app.config["SRV"].get("LDAP", {}))
        except (TypeError, KeyError):
            return

        users = self.get_users()
        if not isinstance(users, dict) or not users:
            return

        for username, userinfo in users.items():
            if "." not in username:
                continue

            if not ldap.get_user(username):
                continue

            ldap.modify_user(username, {
                "telephoneNumber": userinfo["mobile"],
                "displayName": userinfo["name"],
                "mail": userinfo["email"]
            })

        return self.update_task_log("success synced %s users to ldap." % len(users))

    def call_welab_send_sms_api(self, message, command):
        users = self.get_users()

        user = users.get(message["from"])
        res = request("POST", API_SENDER_SMS_ENDPOINT, json={
            "sender": command.get("from"),
            "to": command.get("to"),
            "msg": command.get("message")
        })

        self.send([user["username"]], res.text)

        return self.update_task_log()

    def issue_report_api(self, message, issue, create=True):
        users = self.get_users()

        user = users.get(message["from"], {
            "name": message["from"],
            #: can't get userinfo then send the message to admin
            "username": "Unknow"
        })

        if issue:
            if create:
                ir = IssueReport.add(dict(issue, **{"created_by": user["username"]}))
            else:
                ir = IssueReport.get_by_id(issue["id"])

            if ir.source.endswith("_desktop"):
                if ir.source.startswith("alt1"):
                    location = "地理位置: 阿里大厦[T1]\n"
                elif ir.source.startswith("alt2"):
                    location = "地理位置: 阿里大厦[T2]\n"
                else:
                    location = None

                content = f'IT 问题反馈 - 第【{ir.get_current_day_number()}】单:\n' \
                    f"问题名称: {ir.name}\n" \
                    f'{location if location else ""}' \
                    f"反馈时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                    f"平台链接: https://sa.wolaidai.com/#/issue/index?id={ir.id}&src={ir.source}\n" \
                    f"{'-' * 15}\n" \
                    f"辛苦相关同学尽快协助 【{user['name']}】 处理该问题，谢谢。"

                if ir.source.startswith("lc"):
                    self.push(chat_id="13564560603047281058", content=content)
                elif ir.source.startswith("alt"):
                    self.push(chat_id="11733284404567757764", content=content)
                else:
                    pass
            elif ir.source == "customer_service":
                content = f'客服系统问题反馈 - 第【{ir.get_current_day_number()}】单:\n' \
                    f"问题名称: {ir.name}\n" \
                    f"反馈时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                    f"平台链接: https://sa.wolaidai.com/#/issue/index?id={ir.id}&src={ir.source}\n" \
                    f"{'-' * 15}\n" \
                    f"辛苦相关同学尽快协助 【{user['name']}】 处理该问题，谢谢。"

                self.push(chat_id="15549522138810831813", content=content)
            elif ir.source == "prod":
                content = f'生产环境问题反馈 - 第【{ir.get_current_day_number()}】单:\n' \
                    f"问题名称: {ir.name}\n" \
                    f"反馈时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                    f"平台链接: https://sa.wolaidai.com/#/issue/index?id={ir.id}&src={ir.source}\n" \
                    f"{'-' * 15}\n" \
                    f"请问题相关同学快速处理该问题，谢谢。"

                self.push(chat_id="12481444892664686010", content=content)
            elif ir.source == "other":
                pass
            else:
                content = f'环境问题反馈 - 第【{ir.get_current_day_number()}】单:\n' \
                    f"问题名称: {ir.name}\n" \
                    f"问题环境: {ir.env.upper()}\n" \
                    f"反馈时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                    f"平台链接: https://sa.wolaidai.com/#/issue/index?id={ir.id}&src={ir.source}\n" \
                    f"{'-' * 15}\n" \
                    f"辛苦相关同学尽快协助 【{user['name']}】 处理该问题，谢谢。"

                self.push(chat_id="16424064891450815878", content=content)
        else:
            self.send([user["username"]], "无效的 【环境问题】 模板，请校验你发送的消息或联系运维协助你处理。")
            return self.update_task_log(status=self.failed)

        return self.update_task_log()

    def send_issue_report(self, source):
        split_text = "-" * 35

        total_number = 0
        pending_number = 0
        processed_number = 0
        closed_number = 0
        contents = [split_text]

        if source.startswith("alt"):
            issues = (
                IssueReport.get_all_by_current_day("alt1_desktop") +
                IssueReport.get_all_by_current_day("alt2_desktop")
            )
        else:
            issues = IssueReport.get_all_by_current_day(source)

        for index, issue in enumerate(issues):
            total_number += 1

            if issue.status == 0:
                pending_number += 1
            elif issue.status == 3:
                processed_number += 1
            elif issue.status == 6:
                closed_number += 1

            if issue.status == 0:
                status_text = "待处理"
            elif issue.status == 3:
                status_text = "已处理 - 待关闭"
            elif issue.status == 6:
                status_text = "已处理 - 已关闭"
            else:
                status_text = "-"

            contents.append(
                f"[{index + 1}]: {issue.env.upper()} - {issue.created_by} 发起的 【{issue.name}】- {status_text}"
            )

        if total_number:
            content = f'[{datetime.now().strftime("%Y-%m-%d")}] - 问题处理统计日报\n' \
                f'      - 反馈问题总数 {total_number}\n' \
                f'      - 已完成问题数 {closed_number}\n' \
                f'      - 未处理问题数 {pending_number}\n' \
                f'      - 问题未关闭数 {processed_number}\n\n' \
                f'问题清单：\n' + '\n'.join(contents + [split_text])

            if source.endswith("_desktop"):
                if source.startswith("lc"):
                    self.push(chat_id="13564560603047281058", content=content)
                elif source.startswith("alt"):
                    self.push(chat_id="11733284404567757764", content=content)
                else:
                    pass
            elif source == "customer_service":
                self.push(chat_id="15549522138810831813", content=content)
            else:
                self.push(chat_id="16424064891450815878", content=content)

        return self.update_task_log()

    def ldap_reset_password_api(self, message, auth):
        users = self.get_users()
        user = users.get(message["from"])

        invalid_password_msg = "LDAP 密码重置失败，你的密码格式不合法。"
        ldap_user_no_exist_msg = "LDAP 用户不存在，请联系管理员。"
        ldap_server_err_msg = "LDAP 密码重置失败: %s"

        if not auth.get("password"):
            self.send([user["username"]], invalid_password_msg)
            return self.update_task_log(invalid_password_msg, self.failed)

        ldap = LdapClient(current_app.config["SRV"].get("LDAP", {}))
        if not ldap.get_user(user["username"]):
            self.send([user["username"]],  ldap_user_no_exist_msg)
            return self.update_task_log(ldap_user_no_exist_msg, self.failed)

        result = ldap.reset_password(user["username"], auth["password"])
        if not isinstance(result, dict) or result.get("description") != "success":
            self.send([user["username"]], ldap_server_err_msg % str(result))
            return self.update_task_log(ldap_user_no_exist_msg, ldap_server_err_msg % str(result))

        self.send([user["username"]], "LDAP 密码重置成功")
        return self.update_task_log()

    def aip_speech(self, message):
        users = self.get_users()
        user = users.get(message["from"])
        err_msgs = [
            "不好了，Mr.Lai 出问题了，没听懂您说了啥",
            "哎呀，人类的语言还真复杂，能再说一遍吗？",
            ""
        ]

        media_url = f"{self.base_url}/media/get?access_token={self.get_token()}&media_id={message['media_id']}"
        res = request("GET", media_url)
        if res.headers.get("Content-Type") == "audio/amr":
            aip_config = current_app.config['SRV'].get('AIP')
            aip_client = AipSpeech(aip_config["APP_ID"], aip_config["API_KEY"], aip_config["SECRET_KEY"])

            aip_res = aip_client.asr(res.content, 'amr', 8000, {'dev_pid': 1537})

            if aip_res["err_no"] != 0 or "result" not in aip_res:
                self.send([user["username"]], choice(err_msgs))
                return self.update_task_log(status=self.failed)

            pinyin = ''.join(s for s in '_'.join(lazy_pinyin(aip_res["result"])) if s.isalnum() or s == "_")
            if any(hit in pinyin for hit in ['wen', 'ti', 'fan', 'kui']):
                self.run("ticket", "generate_key", message=message, event_key="1020")
                return self.update_task_log()

            if any(hit in pinyin for hit in ['fa', 'qi', 'chuan', 'cuan', 'qin', 'xin', 'jian']):
                self.run("ticket", "generate_key", message=message, event_key="1001")
                return self.update_task_log()

            if any(hit in pinyin for hit in ['shen', 'sen', 'pi', 'he']):
                self.run("ticket", "generate_key", message=message, event_key="1010")
                return self.update_task_log()

        self.send([user["username"]], choice(err_msgs))
        return self.update_task_log(status=self.failed)

    def send_ticket_pending_audit_notice(self):
        pending_audits = WorkorderTicket.get_all_pending_audit()
        users = self.get_users()

        for pending_audit in pending_audits:
            user = users.get(pending_audit["username"], {"username": "freedie.liu"})
            if not user:
                continue

            launch_key = self.run("ticket", "render_launch_cache_key", userid=user["userid"], event_key="1010")
            cache.set(launch_key, user, timeout=1800)

            self.send(user_list=[user["username"]], content=(
                f'<a href="https://sa.wolaidai.com/#/biz-wechat/ticket/audit?key={launch_key}">'
                f'您好，您在系统里还有 {pending_audit["count"]} 个工单未审批哦，点击本消息开始审批工单吧 [本入口有效期 30 分钟]</a>'
            ))

        return self.update_task_log()

    def send_ticket_pending_validation_notice(self):
        pending_validations = WorkorderTicket.get_all_pending_validation()
        username_titles_dict = {}

        users = self.get_users()
        for pending_validation in pending_validations:
            username_titles_dict[pending_validation["username"]] = username_titles_dict.get(
                pending_validation["username"], []
            )

            username_titles_dict[pending_validation["username"]].append(pending_validation["title"])

        for username, titles in username_titles_dict.items():
            user = users.get(username, {"username": "freedie.liu"})
            self.send(user_list=[user["username"]], content=(
                '工单服务 - 未验证提醒:\n' + ' - 未验证\n'.join(titles + [''])
            ))

    def send_onduty(self, message):
        # onduty_users = ["qi.zhang", "mizhong.huang"]
        self.send(user_list=[message["from"]], content="今日值班人员: Qi张琪")

    @classmethod
    def execute(cls, fn, *args, **kwargs):
        """
        :param str fn: execute function name
        :param list args: execution function required list
        :param dict kwargs: execution function required kwargs
        :return:
        """
        self = cls(current_app.config['SRV'].get('WECHAT'))
        if not (isinstance(fn, str) or not hasattr(self, fn)):
            raise InvalidFnError()

        return getattr(self, fn)(*args, **kwargs)
