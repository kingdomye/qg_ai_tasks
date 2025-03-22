import requests,json
url="http://47.99.82.164/mobile_check"
params={"class_num":"21218710","password":"kingdom666"}
response=requests.get(url=url,params=params)
print(response.text)