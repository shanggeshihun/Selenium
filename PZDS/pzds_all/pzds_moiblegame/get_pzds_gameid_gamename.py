# _*_coding:utf-8 _*_

#@Time      : 2022/5/4  18:03
#@Author    : An
#@File      : get_pzds_gameid_gamename.py
#@Software  : PyCharm

import requests,json

url = 'https://www.pzds.com/api/v2/homepage/public/game/all'

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Host':'www.pzds.com',
    'Origin': 'https://www.pzds.com',
    'Referer': 'https://www.pzds.com/',
    'Content-Type': 'application/json;charset=UTF-8'
}

payload_data = {"action":{}}

req = requests.post(url = url,headers = headers,data = json.dumps(payload_data))

json_loads = json.loads(req.text)

data = json_loads['data']

with open("./gameid_gamename.json",'w+',encoding='utf-8') as f:
    json.dump(data,f )
    # for dict in data:
    #     json.dump(dict,f)
