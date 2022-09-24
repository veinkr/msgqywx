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


class msgqywx:
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
        self.seckey_md5 = md5((self.corpid + self.corpsecret).encode(encoding='utf-8')).hexdigest()
        self.accessconffile = os.path.join("~/.config/msgqywx", f"{self.seckey_md5}.conf")

    def access_token_to_jsonfile(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.corpid,
                  'corpsecret': self.corpsecret,
                  }
        req = requests.post(url, params=values)
        if req.status_code == 200:
            data = json.loads(req.text)
            wite_json = {"cur_time": datetime.now().timestamp(),
                         "access_token": data["access_token"]}
            with open(self.accessconffile, 'w') as f:
                json.dump(wite_json, f)
            return wite_json
        else:
            print(req.text)
            raise Exception("获取企业微信的access_token失败,请检查企业ID（corpid）和应用Secret（corpsecret）是否正确")

    def get_access_token(self):
        try:
            with open(self.accessconffile, 'r') as f:
                access_json = json.load(f)
                cur_time = datetime.now().timestamp()
                if 0 < cur_time - float(access_json["cur_time"]) < 7000:
                    # print("通过文件获取到access_token")
                    return access_json["access_token"]
                else:
                    f.close()
                    return self.access_token_to_jsonfile()["access_token"]
        except FileNotFoundError:
            return self.access_token_to_jsonfile()["access_token"]
        except Exception as err:
            print("未知错误，请告知作者：\n", err)
            return self.access_token_to_jsonfile()["access_token"]

    def send_msg(self, message, msgtype: str = 'text', touser: str = None, raise_error: bool = False):
        """
        send_msg发送文本类消息
        :param msgtype: 消息类型，仅支持 text 和 markdown
        :param raise_error: 是否抛出发送错误(response不等于200的情况)，默认为False
        :param message: 消息内容，当前仅支持文本内容
        :param touser: 发送用户，和初始化类时的touser不能同时为None
        :return: 微信返回的response，可以自行处理错误信息，也可不处理
        """
        touser = touser if touser else self.touser
        if touser is None:
            raise Exception("无发送用户")
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + \
                   self.get_access_token()
        send_values = {
            "touser": touser,
            "agentid": self.agentid,
            "text": {"content": message},
            "markdown": {"content": message},
        }
        if msgtype == 'text':
            send_values["msgtype"] = "text"
            del send_values["markdown"]
        elif msgtype == 'markdown':
            send_values["msgtype"] = "markdown"
            del send_values["text"]
        else:
            raise Exception("不支持的msgtype")

        respone = requests.post(send_url, json=send_values)
        if respone.status_code == 200:
            return respone
        else:
            if raise_error:
                raise Exception(respone.text)
            else:
                return respone
