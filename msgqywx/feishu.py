import requests


class feishu:
    BASE_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/"

    def __init__(self, hook_id):
        self.url = self.BASE_URL + hook_id

    def send(self, message: str, msgtype: str = "text", raise_error=False):
        response = requests.post(
            url=self.url, json={"msg_type": msgtype, "content": {"text": message}}
        )
        if not response.ok and raise_error:
            response.raise_for_status()
        else:
            return response
