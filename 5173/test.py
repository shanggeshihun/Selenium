# _*_coding:utf-8 _*_

#@Time      : 2021/12/25  22:44
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

start_url = 'http://sy.5173.com/BizOffer/GoodsList?GameId=c646190d768f4ab6913ab9d2b8e1ac07&GameCateId=55679ff4503347c8a29749f45075f285&GamePlatformId='
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=driver_path)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
})

from lxml import etree

browser.get(start_url)
html = etree.HTML(browser.page_source)

server_protection =  html.xpath(
            ".//td[@class='serve']/p/text()")
print(server_protection)