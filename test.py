# _*_coding:utf-8 _*_

#@Time      : 2021/12/16  22:39
#@Author    : An
#@File      : get_webgame_info.py
#@Software  : PyCharm

from selenium import webdriver
import time
browser = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')

#访问百度首页
first_url = "http://www.baidu.com"#定义一个变量，将网页指向
browser.get(first_url)# 打开浏览器，及页面
time.sleep(3)

#访问新闻首页
second_url = "http://news.baidu.com/"#定义一个变量，将网页指向
print("打开 %s"%(second_url))#打印网页的操作动向
browser.get(second_url)# 打开浏览器，及页面
time.sleep(3)

#返回，后退到百度首页
print("back to %s"%(first_url))#打印网页的操作动向
browser.back()#后退
time.sleep(3)

#前进到新闻页面
print("forard to %s"%(second_url))#打印网页的操作动向
browser.forward()# #前进
time.sleep(2)
browser.refresh()
time.sleep(2)

browser.quit() #关闭


import pandas as pd
df = pd.DataFrame()

df.to_sql()