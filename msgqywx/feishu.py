import requests


class feishu:
    BASE_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/"

    def __init__(self, hook_id, retry=1):
        self.url = self.BASE_URL + hook_id
        self.retry = retry

    def send(self, message: str, msgtype: str = "text", retry=None, raise_error=False):
        retry = retry or self.retry
        for i in range(retry):
            response = requests.post(
                url=self.url, json={"msg_type": msgtype, "content": {"text": message}}
            )
            if response.ok:
                return response
        else:
            if raise_error:
                response.raise_for_status()
            else:
                return response
