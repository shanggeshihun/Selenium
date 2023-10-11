# _*_coding:utf-8 _*_

#@Time      : 2021/12/17  12:42
#@Author    : An
#@File      : 11前进后退.py
#@Software  : PyCharm

# -*- coding:utf-8 -*-
#导入webdrive
from selenium import webdriver
import time

browser = webdriver.Chrome()#定义驱动浏览器

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