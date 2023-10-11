# _*_coding:utf-8 _*_

#@Time      : 2021/12/21  15:39
#@Author    : An
#@File      : get_webgame_info.py
#@Software  : PyCharm


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv,pymysql,threading
from queue import  Queue
from lxml import etree
game_url_queue = Queue()
# 解析队列
item_parse_queue = Queue()

start_url = 'https://www.dd373.com/s-49pbxm-c-vrhh20.html'
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=driver_path)
browser.get(start_url)
page_source = browser.page_source

html = etree.HTML(page_source)
goods_list_item = html.xpath("//div[@class = 'goods-list-item']")
for item_box in goods_list_item:
    title = item_box.xpath(".//div[@class= 'game-account-flag']/text()")
    i = 0
    re = ''.join([t.strip().replace("\n","") for t in title])
    print(re)
    break
