# msgqywx

使用企业微信的应用消息推送实时信息

### Install

```
pip install git+https://github.com/veink-y/msgqywx.git
```

### Params

- corpid: 企业ID，在管理后台获取
- corpsecret: 自建应用的Secret，每个自建应用里都有单独的secret
- agentid: 应用ID，在后台应用中获取
- touser: 接收者用户名(微信账号),多个用户用|分割

### Usage

```python
from msgqywx import msgqywx

if __name__ == '__main__':
    wx = msgqywx(corpid='ww7e42424723224ba8ff49',
                 corpsecret='we0YB4242424242_J2332PnmA',
                 agentid='2115353',
                 touser='xxxxxxxxxx',
                 )
    wx.send_msg("这是测试信息")  # 使用初始类的touser
    wx.send_msg("这是另一个测试消息", touser="xxxxx")  # 自定义接收的账号

```
