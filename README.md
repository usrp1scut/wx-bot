## 基于wxauto的个人微信助手
* [wxauto gtihub地址](https://github.com/cluic/wxauto)基于里面的demo实现的
* [wxauto官网](https://wxauto.loux.cc/)

### 实现功能（都没啥用，弄着玩）
* 1.接入openai实现AI问答,AI绘图
* 2.配置RSS订阅，根据关键词获取前10条
* 3.配置通过openweathermap获取指定城市的天气
* 4.将实时获取当前电脑的IPv6地址，方便实时连接家庭共享或远程桌面
* 5.推送指定路径随机音乐
### 运行环境

* Windows 10|11|2016+
* Python：3.7+（不支持3.7.6和3.8.1）

需要保持桌面渲染，物理机需要保持显示输出，虚拟机要在虚拟控制台里面执行，rdp执行的断开连接后会停止

### 安装依赖
```
pip install wxauto openai python-dotenv pyowm feedparser
```
### 运行
先运行微信，微信版本要求见wxauto
```
python run.py
```
