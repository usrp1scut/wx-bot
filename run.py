from llm import GPT
from wxauto import WeChat
import os
import random
import time
import socket
from dotenv import load_dotenv
import feedparser
from pyowm import OWM
from pyowm.utils.config import get_default_config
import urllib.request

#配置rss订阅关键词及url
rsslist = {
    "中新网": "https://www.chinanews.com.cn/rss/scroll-news.xml",
    "IT之家": "https://www.ithome.com/rss/",
    "网络安全": "https://www.freebuf.com/feed",
    "雪球话题": "https://xueqiu.com/hots/topic/rss",
    "豆瓣书评": "https://www.douban.com/feed/review/book"
}

# 指定监听目标
listen_list = [
    '张三',
    '李四',
    '家庭群',
    '工作群'
]

def get_weather():
    config_dict = get_default_config()
    config_dict['language'] = 'zh_cn'
    config_dict['connection']['use_proxy'] = True
    config_dict['proxies']['http'] = os.getenv('HTTP_PROXY')
    config_dict['proxies']['https'] = os.getenv('HTTPS_PROXY')
    owm = OWM('fdf47cd18a688cba4edaaf04c7689472',config_dict)
    # 获取天气管理器
    mgr = owm.weather_manager()
    # 获取环境变量中指定城市的天气信息
    city = os.getenv('MY_CITY')
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    return weather

#下载AI绘图图片
def download_image(url, file_name):
    urllib.request.urlretrieve(url, file_name)
    print("图片下载成功！")

#获取随机音乐
def get_music():
    folder_path = 'E:\music'
    # 获取文件夹中的所有文件名
    filenames = os.listdir(folder_path)
    # 随机选择一个文件
    random_filename = random.choice(filenames)
     
    # 完整路径
    random_file_path = os.path.join(folder_path, random_filename)
    return random_file_path

#获取RSS订阅前10条
def rss(url):
    news_str = ''
    file = feedparser.parse(url)
    count = 10 
    for i in file.entries:
        count = count - 1
        news_str = news_str + "* " + i.title + '\n' + i.link + '\n'
        if count == 0:
            break
    return news_str

#获取当前IPv6
def get_ip_addresses():
    ip_addresses = []
    # 获取本机所有网络接口的信息
    hostname = socket.gethostname()
    try:
        # 获取 IPv6 地址 
        for ip in socket.getaddrinfo(hostname,None, socket.AF_INET6):
            ip_addresses.append(ip[4][0])
    except Exception as e:
        print(f"获取 IP 地址时发生错误: {e}")
    return ip_addresses[1]

# 读取相关环境变量
load_dotenv()
cfg = open('config.txt','r')

# 初始化GPT模型
gpt = GPT(
    api_key = os.getenv('OPENAI_API_KEY'),
    base_url = os.getenv('OPENAI_BASE_URL'),
    prompt="你是一个严肃认真的智能问答助手，有理有据地回答问题"
)


wx = WeChat()

image_save = 'E:\\code\\image.png'

for i in listen_list:
    wx.AddListenChat(who=i,savepic = False,savefile = False,savevoice = False )  # 添加监听对象
    

# 持续监听消息，有消息则对接大模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            try:
                one_msgs = msgs.get(chat)   # 获取消息内容
                print(one_msgs)
                for msg in one_msgs:
                        if msg.type == 'friend':
                            sender = msg.sender # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                            if msg.content in rsslist.keys():
                                news = rss(rsslist[msg.content])
                                chat.SendMsg(news)
                            elif msg.content == '音乐':
                                music = get_music()
                                chat.SendFiles(music.replace("\\","\\\\"))
                            elif msg.content == '天气':
                                weather = get_weather()
                                chat.SendMsg(f"环境温度：{weather.temperature('celsius')['temp']}°C" + '\n' + f"体感温度：{weather.temperature('celsius')['feels_like']}°C" + '\n' + f"{weather.detailed_status}")
                            #当你的电脑同时作为家庭共享文件夹时，可以通过此功能获取共享文件夹的动态IPv6地址，我这里有movie和music两个共享文件夹
                            elif msg.content == '共享文件夹':
                                share_ip = get_ip_addresses()
                                share_link = share_ip.replace(":","-")
                                movie = "\\\\" + share_link + ".ipv6-literal.net\movie"
                                music = "\\\\" + share_link + ".ipv6-literal.net\music"
                                chat.SendMsg("共享IP   " + share_ip + '\n' )
                                chat.SendMsg('windows链接:\n' + movie + '\n' + music )
                            elif '@AI'in msg.content :
                                reply = gpt.chat(msg.content.replace("@AI",""))
                                chat.SendMsg(reply)
                            elif '作图' in msg.content:
                                url = gpt.draw(msg.content.replace("作图",""))
                                download_image(url,image_save)
                                chat.SendFiles(image_save)
                                #chat.SendMsg(url)
            except:
                continue

