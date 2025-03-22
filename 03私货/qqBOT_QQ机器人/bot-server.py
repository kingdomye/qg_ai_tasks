from flask import Flask, request
import requests
import time
import random
import json
from pypinyin import lazy_pinyin
id = str(random.randint(0,200))
now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
def get_wheather(city):
    temp=lazy_pinyin(city)
    temp1=""
    for i in temp:
        temp1=temp1+i
    now_wheather_info=requests.get(f'https://api.seniverse.com/v3/weather/now.json?key=SEetFUxr6EqAL_CQB&location={temp1}&language=zh-Hans&unit=c').text
    now_wheather_info=json.loads(now_wheather_info)
    now_wheather_results=now_wheather_info["results"][0]
    now_wheather_information=now_wheather_results["now"]
    now_wheather=now_wheather_information["text"]
    now_temperature=now_wheather_information["temperature"]
    wheather=city+"  "+now_wheather+" "+now_temperature+"℃"
    return wheather


app = Flask(__name__)
@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get('message_type') == 'private':  # 私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        if message=="菜单":
            message='YR-BOT菜单\n\n1、城市天气\n2、功能2\n3、功能3\n4、功能4\n5、功能5\n6、功能6\n7、功能7\n\n更多精彩尽在\nwww.wzyuying.icu'
            requests.get(url=f'http://127.0.0.1:5700/send_private_msg?user_id={uid}&message={message}')
        if message=="1" or message==1:
            requests.get(url=f'http://127.0.0.1:5700/send_private_msg?user_id={uid}&message=示例：城市天气 北京')
        if message[0:4]=="城市天气":
            city=message.split(" ")[1]
            wheather=get_wheather(city)
            requests.get(url=f'http://127.0.0.1:5700/send_private_msg?user_id={uid}&message={wheather}')

    if request.get_json().get('message_type')=='group':# 如果是群聊信息
        gid = request.get_json().get('group_id') # 获取群号
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        if message=="菜单":
            if gid==1170353595 or gid==853898478:
                message='YR-BOT菜单\n\n1、城市天气\n2、功能2\n3、功能3\n4、功能4\n5、功能5\n6、功能6\n7、功能7\n\n更多精彩尽在\nwww.wzyuying.icu'
                requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={message}')
        if message=="1" or message==1:
            requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message=示例：城市天气 北京')
        if message[0:4]=="城市天气":
            city=message.split(" ")[1]
            wheather=get_wheather(city)
            requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={wheather}')

    return "None"

if __name__ == '__main__':
    requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id=3356203629&message=YR机器人正常开机！'+now_time+f'[CQ:face,id={id}]')
    app.run(host='127.0.0.1', port=5701)  # 此处的 host和 port对应上面 yml文件的设置