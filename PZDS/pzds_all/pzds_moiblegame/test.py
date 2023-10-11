# _*_coding:utf-8 _*_

# @Time      : 2021/12/27  9:28
# @Author    : An
# @File      : get_webgame_info.py
# @Software  : PyCharm


import sys,datetime
today = (datetime.datetime.now()).strftime('%Y-%m-%d')  # 今日日期
today_hour = (datetime.datetime.now()).strftime('%H')  # 今日日期小时
print(int(today_hour))