import requests
import json
import wget
import os
def bing_images():
    data=json.loads(requests.get("https://raw.onmicrosoft.cn/Bing-Wallpaper-Action/main/data/zh-CN_all.json").text)["data"]
    for i in data:
        url="https://www.bing.com"+i["url"]
        print(url)
bing_images()