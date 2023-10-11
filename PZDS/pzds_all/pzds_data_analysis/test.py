# _*_coding:utf-8 _*_

# @Time      : 2022/5/11  14:43
# @Author    : An
# @File      : schedule_test.py
# @Software  : PyCharm
import re

def regexp():
    pattern = re.compile(r"【(.*?)(QQ|微信).*】.*【(.*?)】\s*贵族(\d+)\s*荣耀水晶(\d+)\s*英雄(\d+)\s*皮肤(\d+)\s*(.*?)\s*营地.*?(\d+)")
    ss = "C40015 号  【苹果微信112区】【可二次实名】 贵族10 荣耀水晶6 英雄109 皮肤322 至尊星耀II 营地:78708613   "
    res = pattern.findall(ss)
    print(res)

if __name__ == '__main__':
    regexp()