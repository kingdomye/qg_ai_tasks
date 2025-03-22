import requests
import json
def 今日热点():
    sum="今日热点\n------------------\n"
    num=0
    url="https://v.api.aa1.cn/api/topbaidu/index.php"
    newslist=json.loads(requests.get(url).text)["newslist"]
    for i in newslist:
        num+=1
        if num==6:
            break
        sum+=i["title"]+" | "+"热度"+str(i["hotnum"])+"\n"+i["digest"]+"\n------------------\n"
    return sum
a=今日热点()
print(a)