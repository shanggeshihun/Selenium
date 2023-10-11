# _*_coding:utf-8 _*_

#@Time      : 2022/5/4  18:31
#@Author    : An
#@File      : read_json.py
#@Software  : PyCharm

import json

with open('./gameid_gamename.json','r') as f:
    gameid_gamename_list = json.load(f)
    print(gameid_gamename_list)