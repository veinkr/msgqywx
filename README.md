# msgqywx

使用企业微信的应用消息推送实时信息

注：markdown支持无法在微信中查看

### Install

```
pip install msgqywx
```

### Params

- corpid: 企业ID，在管理后台获取
- corpsecret: 自建应用的Secret，每个自建应用里都有单独的secret
- agentid: 应用ID，在后台应用中获取
- touser: 接收者用户名(微信账号),多个用户用|分割,与发送消息的touser至少存在一个

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

    md_text = """您的会议室已经预定，稍后会同步到`邮箱`
                >**事项详情**
                >事　项：<font color=\"info\">开会</font>
                >组织者：@miglioguan
                >参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang
                >
                >会议室：<font color=\"info\">广州TIT 1楼 301</font>
                >日　期：<font color=\"warning\">2018年5月18日</font>
                >时　间：<font color=\"comment\">上午9:00-11:00</font>
                >
                >请准时参加会议。
                >
                >如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)"""
    wx.send_msg(md_text, msgtype="markdown", raise_error=True)  # 发送markdown消息，注意markdown消息仅企业微信可接收
```

### Limit

##### 基础频率

> 每企业调用单个cgi/api不可超过1万次/分，15万次/小时;  
> 每ip调用单个cgi/api不可超过2万次/分，60万次/小时;  
> 第三方应用提供商每ip调用单个cgi/api不可超过4万次/分，120万次/小时;

##### 发送应用消息频率

> 每应用不可超过帐号上限数*200人次/天（注：若调用api一次发给1000人，算1000人次；若企业帐号上限是500人，则每个应用每天可发送100000人次的消息）;  
> 每应用对同一个成员不可超过30次/分钟，超过部分会被丢弃不下发;  
> 发消息频率不计入基础频率;  
