# _*_coding:utf-8 _*_

#@Time      : 2021/12/20  16:45
#@Author    : An
#@File      : test_find.py
#@Software  : PyCharm


from selenium import webdriver
import time, csv

driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(executable_path=driver_path)
url = 'https://search.7881.com/list.html?pageNum=1&gameId=G5209&gtid=100003'
browser.get(url)
aa= browser.page_source.find('抱歉，没有找到相关商品')
print(aa)
