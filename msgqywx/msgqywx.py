# -*- coding:utf-8 -*-
"""
filename : msgqywx.py
createtime : 2021/6/20 21:46
author : Demon Finch
"""
import os
import json
import requests
from hashlib import md5
from datetime import datetime


class UserError(Exception):
    ...


class msgqywx:
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

    def __init__(self, corpid: str, corpsecret: str, agentid: str, touser: str = None):
        """
        发送企业微信应用消息
        :param corpid: 企业ID，在管理后台获取
        :param corpsecret: 自建应用的Secret，每个自建应用里都有单独的secret
        :param agentid: 应用ID，在后台应用中获取
        :param touser: 接收者用户名(微信账号),多个用户用|分割，与发送消息的touser至少存在一个
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.touser = touser
        self.secret_key_md5 = md5(
            (self.corpid + self.corpsecret).encode(encoding="utf-8")
        ).hexdigest()
        self.base_config_folder = f"{os.path.expanduser('~')}/.config/msgqywx"
        if not os.path.exists(self.base_config_folder):
            os.makedirs(self.base_config_folder)
        self.access_conf_file = os.path.join(
            self.base_config_folder, f"{self.secret_key_md5}.conf"
        )

    def access_token_to_jsonfile(self):

        values = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret,
        }
        response = requests.post(self.url, params=values)
        if response.ok:
            data = json.loads(response.text)
            secret_json = {
                "expire_time": datetime.now().timestamp() + 3600,
                "access_token": data["access_token"],
            }
            with open(self.access_conf_file, "w") as f:
                json.dump(secret_json, f)
            return secret_json
        else:
            print(response.text)
            raise Exception(
                "获取企业微信的access_token失败,请检查企业ID（corpid）和应用Secret（corpsecret）是否正确"
            )

    def get_access_token(self):
        if os.path.exists(self.access_conf_file):
            with open(self.access_conf_file, "r") as f:
                access_json = json.load(f)
                if access_json.get("expire_time", 0) > datetime.now().timestamp():
                    return access_json["access_token"]
                else:
                    f.close()
                    return self.access_token_to_jsonfile()["access_token"]
        else:
            return self.access_token_to_jsonfile()["access_token"]

    def send_msg(
        self,
        message,
        msgtype: str = "text",
        touser: str = None,
        raise_error: bool = False,
    ):
        """
        send_msg发送文本类消息
        :param msgtype: 消息类型，仅支持 text 和 markdown
        :param raise_error: 是否抛出发送错误(response不等于200的情况)，默认为False
        :param message: 消息内容，当前仅支持文本内容
        :param touser: 发送用户，和初始化类时的touser不能同时为None
        :return: 微信返回的response，可以自行处理错误信息，也可不处理
        """
        if msgtype not in ["text", "markdown"]:
            raise TypeError(
                "Unsupported msgtype, only `text` and `markdown` are acceptable"
            )

        touser = touser if touser else self.touser  # use or
        if touser is None:
            raise UserError("touser must not None")

        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )  # use f-string
        payload = {
            "touser": touser,
            "agentid": self.agentid,
            "msgtype": msgtype,
            msgtype: {"content": message},
        }

        response = requests.post(send_url, json=payload)
        if not response.ok and raise_error:
            response.raise_for_status()
        else:
            return response
