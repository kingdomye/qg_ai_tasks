import random
import sqlite3

import pandas as pd
import requests
from openai import OpenAI


def get_random_sentence():
    url = "https://xiaoapi.cn/API/yiyan.php"
    try:
        response = requests.get(url)
        data = response.text
    except:
        data = "ERROR"
    return data


def test_random_sentence():
    type_list = ['动漫', '鼓励', '孤独', '搞笑', '友情', '歌词']
    rnd_type = random.choice(type_list)
    url = f"https://xiaoapi.cn/API/yulu.php?type={rnd_type}"
    response = requests.get(url)
    data = response.text
    return data


def get_weather(city):
    future_weather_url = "https://api.seniverse.com/v3/weather/daily.json"
    living_suggest_url = "https://api.seniverse.com/v3/life/suggestion.json"

    params = {
        "key": 'SEetFUxr6EqAL_CQB',
        "location": city,
        "language": "zh-Hans",
        "unit": "c"
    }

    try:
        future_weather_response = requests.get(future_weather_url, params=params)
        living_suggest_response = requests.get(living_suggest_url, params=params)

        future_weather_data = future_weather_response.json()['results'][0]['daily']
        living_suggest_data = living_suggest_response.json()['results'][0]['suggestion']

        res = f'==={city}天气===\n'
        for item in future_weather_data:
            res += f'{item["date"]} {item["text_day"]} {item["high"]}℃/{item["low"]}℃\n'

        res += f'\n==={city}生活建议===\n'
        res += f'洗车: {living_suggest_data["car_washing"]["brief"]}\n'
        res += f'穿衣: {living_suggest_data["dressing"]["brief"]}\n'
        res += f'感冒: {living_suggest_data["flu"]["brief"]}\n'
        res += f'运动: {living_suggest_data["sport"]["brief"]}\n'
        res += f'旅游: {living_suggest_data["travel"]["brief"]}\n'
        res += f'紫外线: {living_suggest_data["uv"]["brief"]}'
    except:
        res = "YR-BOT查询不到该城市喔，换个城市再试试吧！😘"

    res += "\n\n" + test_random_sentence()
    return res


def search_users():
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data")
    users = cursor.fetchall()
    db.close()
    print(users)


def show_homework():
    res = "===本周班级作业===\n"
    try:
        file = pd.read_excel('./excel/homework.xlsx')
        df = pd.DataFrame(file)
        for i in range(len(df)):
            res += f'{i + 1}、{df.iloc[i, 0]}：{df.iloc[i, 1]}\n'
    except:
        res += "作业查询失败！"

    res += "\n" + test_random_sentence()

    return res


def add_homework(type, content):
    try:
        file = pd.read_excel('./excel/homework.xlsx')
        df = pd.DataFrame(file)
        df.loc[len(df)] = [type, content]
        df.to_excel('./excel/homework.xlsx', index=False)
        print("添加成功")
    except:
        print("添加失败")


def delete_homework(index):
    try:
        file = pd.read_excel('./excel/homework.xlsx')
        df = pd.DataFrame(file)
        df = df.drop(index - 1)
        df.to_excel('./excel/homework.xlsx', index=False)
        print("删除成功")
    except:
        print("删除失败")


def clear_homework():
    df = pd.DataFrame(columns=['type', 'content'])
    df.to_excel('./excel/homework.xlsx', index=False)
    print("清空成功")


def show_notice():
    res = "===近日班级通知===\n"
    try:
        file = pd.read_excel('./excel/notice.xlsx')
        df = pd.DataFrame(file)
        for i in range(len(df)):
            res += f'{i + 1}、{df.iloc[i, 0]}\n活动（截止）日期：{df.iloc[i, 1]}\n'

        res += "\n" + test_random_sentence()
    except:
        res += "通知查询失败！"

    return res


def add_notice(content, date):
    file = pd.read_excel('./excel/notice.xlsx')
    df = pd.DataFrame(file)
    df.loc[len(df)] = [content, date]
    df.to_excel('./excel/notice.xlsx', index=False)
    print("添加成功")


def delete_notice(index):
    file = pd.read_excel('./excel/notice.xlsx')
    df = pd.DataFrame(file)
    df = df.drop(index - 1)
    df.to_excel('./excel/notice.xlsx', index=False)
    print("删除成功")


def show_class(day):
    res = "===今日班级课表===\n"
    file = pd.read_excel('./excel/class.xlsx')
    df = pd.DataFrame(file)
    idx = 1
    for i in range(len(df)):
        if df.星期[i] == day:
            res += f'{idx}、{df.iloc[i, 0]}：{df.iloc[i, 7]}\n'
            idx += 1

    res += "\n" + test_random_sentence()

    return res


#Code by lizhengyang
#参数m  1.重复  2.不重复
#参数x  数量
def call(m, x):
    data = pd.read_excel('./excel/name.xlsx')
    data2 = data['姓名']  #获取名字那一列
    n = len(data2)
    data3 = [data2.loc[i] for i in range(n)]  #转化为列表，（因为我不会操作loc[害怕]）
    if m == '重复':
        if x > 100:
            return "太多了🔥🥵🔥,重复抽取上限人数为100喵Ψ(￣∀￣)Ψ\nCode by LZY"
        roster = list(map(int, random.choices(range(0, n), k=x)))
        #创建中奖序列
        sel_ros = [data3[i] for i in roster]
        sel_ros = f"抽奖完成喵Ψ(￣∀￣)Ψ\n--*--{"--*--\n--*--".join(sel_ros)}--*--"

        sel_ros += "\nCode by LZY"
        return sel_ros
    if m == '不重复':
        if x > n:
            return f'太多了🔥🥵🔥,可选数量上限为{n}喵Ψ(￣∀￣)Ψ\nCode by LZY'
        roster = list(map(int, random.sample(range(0, n), k=x)))
        # 创建中奖序列
        sel_ros = [data3[i] for i in roster]
        sel_ros = f"抽奖完成喵Ψ(￣∀￣)Ψ\n--*--{"--*--\n--*--".join(sel_ros)}--*--"

        sel_ros += "\nCode by LZY"
        return sel_ros


def show_fees():
    res = "===本学期班费记录===\n"
    try:
        file = pd.read_excel('./excel/fees.xlsx')
        df = pd.DataFrame(file)
        fees_in = df['in'].sum()
        res += f'【收入】+{int(fees_in) * 38}元\n【支出】\n'

        for i in range(len(df['out'])):
            res += f'{i + 1}、{df['for'][i]}:-{df['out'][i]}元\n'

        fees_out = df['out'].sum()
        res += f'【剩余】{int(fees_in) * 38 - int(fees_out)}元\n'
    except:
        res += "查询失败！"

    res += "\n" + test_random_sentence()
    return res


def chat(msg, history):
    try:
        client = OpenAI(
            api_key="sk-MmuDeFss1XKXOsShdhEn6DebBynbdotvydSmbLx8bY42yKEr",
            # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
            base_url="https://api.moonshot.cn/v1",
        )

        history.append({
            "role": "user",
            "content": msg
        })

        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=history,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        history.append({
            "role": "assistant",
            "content": result
        })

        if len(history) > 10:
            history.pop(1)
        return result
    except:
        return "聊天失效... ..."


if __name__ == '__main__':
    print(get_random_sentence())
