# _*_coding:utf-8 _*_

# @Time      : 2022/5/10  18:49
# @Author    : An
# @File      : schedule_test.py
# @Software  : PyCharm

with open("./mobilegame_info.txt",'r',encoding='utf-8') as f:
    game_url = [line.split(',')[2].strip() for line in f.readlines()]
    print(game_url)