'''
第三方库------------------------------------------------------------------------------------------------------------------------------------------------------------------------
flask , requests , datatime , json , time , openai , random
'''
from flask import Flask, request
import requests
from datetime import datetime
import json
import time
import openai
import random

'''
初始化---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
openai.api_key = "sk-ccfUdWo03FNwcjCWNkkwYKBdL0iztqFlp7hxaesH4FR9GKuU"
openai.api_base = "https://api.chatanywhere.com.cn/v1"
menu="         ✨YR-BOT 菜单✨\n\n群管设置|系统设置|其他设置\n\n每日一言|安慰文案|舔狗日记\n\n搞笑语录|城市天气|今日热点\n\n网易音乐|ChatGPT |敬请期待"
app = Flask(__name__)

'''
定义函数-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
#生成chatgpt访问KEYS
#数量：10;长度：10
def create_keys():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    KEYS = ["YRkey-" + ''.join(random.choice(letters) for _ in range(10)) for _ in range(10)]
    return KEYS
KEYS = create_keys()

def 天气(city):
    url = f'https://v.api.aa1.cn/api/api-tianqi-3/index.php?msg={city}&type=1'
    response = requests.get(url)
    data = response.json()["data"]
    weather_info = []
    for entry in data:
        weather_info.append({
            "日期": entry["riqi"],
            "温度": entry["wendu"],
            "天气": entry["tianqi"],
            "风度": entry["fengdu"],
            "PM2.5": entry["pm"]
        })
    return weather_info

def 今日热点():
    url = "https://v.api.aa1.cn/api/topbaidu/index.php"
    response = requests.get(url)
    newslist = response.json()["newslist"]
    hot_news = "今日热点TOP5\n------------------\n"
    for i, news in enumerate(newslist[:5]):
        hot_news += f"{news['title']} | 热度{news['hotnum']}\n{news['digest']}\n------------------\n" 
    return hot_news

'''
路由-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
@app.route('/', methods=["GET","POST"])
def post_data():
        if request.get_json().get('message_type') == 'private': 
            url="http://127.0.0.1:5700/send_private_msg"
            params = {'user_id': None,
                      'message':None }
            uid = request.get_json().get('sender').get('user_id') 
            message = request.get_json().get('message')
            params["user_id"]=uid
            if message=="菜单":
                now = datetime.now()
                formatted_time = now.strftime("%m月%d日%H时%M分%S秒")
                params["message"]=menu+"\n\n"+formatted_time
                requests.get(url,params=params)
            elif message[0:7].lower() in ["chatgpt"] or message[0:3].lower() in ["gpt"]:
                if message.lower() in ["chatgpt"]:
                    params["message"] = "[参数示例]\nchatgpt KEY 问题\n[注]参数之间使用空格分开，其中KEY表示您向开发者申请的KEY"
                    requests.get(url, params=params)
                else:
                    KEY = message.split(" ")[1]
                    QUE = " ".join(message.split(" ")[2:])
                    data = [{"role": "user", "content": QUE}]
                    if KEY not in KEYS:
                        params["message"] = "KEY填写错误，请向管理员或开发者申请KEY！"
                        requests.get(url, params=params)
                    else:
                        KEYS.remove(KEY)
                        if len(KEYS) <= 5:
                            create_keys()
                        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=data)
                        params["message"] = completion.choices[0].message.content
                        requests.get(url, params=params)
                return "none"

            elif message in ["kingdom321"]:
                params["message"]=random.choice(KEYS)
                requests.get(url,params=params)
            elif message in ["kingdom123"]:
                sum=""
                for item in KEYS:
                    sum=sum+item+"\n\n"
                sum=sum+"YRkey剩余数量: "+str(len(KEYS))
                params["message"]=sum
                requests.get(url,params=params)
            elif message[0:4] in ["网易音乐","音乐"]:
                if message in ["网易音乐","音乐"]:
                    params["message"]="示例\n网易音乐 1454647\n[注]用空格分开，数字代表歌曲id"
                    requests.get(url,params=params)
                else:
                    id=message.split(" ")[1]
                    params["message"]=f'[CQ:music,type=163,id={id}]'
                    requests.get(url,params=params)
            elif message in ["肉色"]:
                data=json.loads(requests.get("https://api.lolicon.app/setu/v2").text)["data"][0]["urls"]["original"]
                CQ="[CQ:image,file=URL]"
                params["message"]=CQ.replace("URL",data)
                requests.get(url,params=params)
            elif message in ["今日热点","热点"]:
                params["message"]=今日热点()
                requests.get(url,params=params)
            elif message in ["每日一言","一言"]:
                text="[一言]   "+requests.get("https://v.api.aa1.cn/api/yiyan/index.php").text
                text=text.replace("<p>","");text=text.replace("</p>","")
                params["message"]=text
                requests.get(url,params=params)
            elif message in ["安慰文案","安慰"]:
                params["message"]=="[安慰文案]   "+json.loads(requests.get("https://v.api.aa1.cn/api/api-wenan-anwei/index.php?type=json").text)["anwei"]
                a=requests.get(url,params=params)
            elif message in ["舔狗日记"]:
                now = datetime.now()
                formatted_time = now.strftime("%m月%d日")
                text="[舔狗日记]   "+formatted_time+"\n"+requests.get("https://v.api.aa1.cn/api/tiangou/index.php").text
                params["message"]=text.replace("<p>","");text=text.replace("</p>","")
                a=requests.get(url,params=params)
            elif message in ["搞笑语录"]:
                params["message"]="[搞笑语录]   "+json.loads(requests.get("https://v.api.aa1.cn/api/api-wenan-gaoxiao/index.php?aa1=json").text)[0]["gaoxiao"]
                requests.get(url,params=params)
            elif "城市天气" in message:
                if message in ["城市天气"]:
                    params["message"]="示例：\n城市天气 北京\n[注]中间使用空格分开"
                    requests.get(url,params=params)
                else:
                    params["message"]=天气(message.split(" ")[1])
                    requests.get(url,params=params)

        if request.get_json().get('message_type') == 'group': 
            time.sleep(1)
            gid = request.get_json().get('group_id')  # 获取群号
            uid = request.get_json().get('sender').get('user_id') 
            message = request.get_json().get('raw_message')
            if message=="菜单":
                now = datetime.now()
                formatted_time = now.strftime("%m月%d日%H时%M分%S秒")
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={menu}\n\n-{formatted_time}'
                requests.get(url)
            elif message in ["全体禁言"]:
                url = "http://127.0.0.1:5700/set_group_whole_ban?group_id={gid}"
                requests.get(url)
            elif message in ["每日一言","一言"]:
                text="[一言]   "+requests.get("https://v.api.aa1.cn/api/yiyan/index.php").text
                text=text.replace("<p>","")
                text=text.replace("</p>","")
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={text}'
                requests.get(url)
            elif message in ["安慰文案","安慰"]:
                text="[安慰文案]   "+json.loads(requests.get("https://v.api.aa1.cn/api/api-wenan-anwei/index.php?type=json").text)["anwei"]
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={text}'
                requests.get(url)
            elif message in ["舔狗日记"]:
                now = datetime.now()
                formatted_time = now.strftime("%m月%d日")
                text="[舔狗日记]   "+formatted_time+"\n"+requests.get("https://v.api.aa1.cn/api/tiangou/index.php").text
                text=text.replace("<p>","")
                text=text.replace("</p>","")
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={text}'
                requests.get(url)
            elif message in ["搞笑语录"]:
                text="[搞笑语录]   "+json.loads(requests.get("https://v.api.aa1.cn/api/api-wenan-gaoxiao/index.php?aa1=json").text)[0]["gaoxiao"]
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={text}'
                requests.get(url)
            elif "城市天气" in message:
                if message in ["城市天气"]:
                    url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message=示例：\n城市天气 北京\n[注]中间使用空格分开'
                    requests.get(url)
                else:
                    tmp=message.split(" ")
                    text=天气(tmp[1])
                    url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={text}'
                    requests.get(url)
            elif message in ["肉色"]:
                data=json.loads(requests.get("https://api.lolicon.app/setu/v2").text)["data"][0]["urls"]["original"]
                CQ="[CQ:image,file=URL,type=show,id=40004]"
                CQ=CQ.replace("URL",data)
                url = f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={CQ}'
                requests.get(url)
        return "none"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5701)