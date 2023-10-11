# _*_coding:utf-8 _*_

#@Time      : 2021/12/26  21:55
#@Author    : An
#@File      : all_game_start_url.py
#@Software  : PyCharm

"""
1 下拉框 selenium 报错
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv,pymysql,threading
from queue import  Queue
from lxml import etree

start_url = 'http://www.5173.com/'
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

from selenium.webdriver.support.select import  Select
# 【游戏名称】下拉框
browser.get(start_url)
time.sleep(4)
spinner_button = browser.find_element_by_xpath("//div[@id='multipleSearch']/ul/li[@id='gs_game' and @class = 'gs_name arrow']")
spinner_button.click()
time.sleep(1)
#
# # 【网络游戏】模块
# netgame_button = browser.find_element_by_xpath("//li[@id = 'netgame']")
# netgame_button.click()
# time.sleep(1)
#
# game_name_list = browser.find_element_by_xpath("//ul[@class='gs_list gs_name']/li/a")
# game_name_list=[game_name.text for game_name in game_name_list]
# len_game_name_list = len(game_name_list)
#
# game_name_url_list = []
# i = 0
# while i<len_game_name_list:
#     # 【游戏名称】下拉框
#     browser.get(start_url)
#     spinner_button = browser.find_element_by_xpath("//ul[@id='gs_game' and @class = 'gs_name arrow']")
#     spinner_button.click()
#     time.sleep(1)
#
#     # 【网络游戏】模块
#     netgame_button = browser.find_element_by_xpath("//li[@id = 'netgame']")
#     netgame_button.click()
#     time.sleep(1)
#
#     game_name_list = browser.find_element_by_xpath("//ul[@class='gs_list gs_name']/li/a")
#     game_name_list = [game_name.text for game_name in game_name_list]
#     len_game_name_list = len(game_name_list)
#
#     # 单个网络游戏
#     game_name_button = browser.find_element_by_xpath("//ul[@class='gs_list gs_name']/li[@lang='netgame']")[i]
#     game_name_button.click()
#
#     search_button = browser.find_element_by_xpath("//input[@id='gsSearchBtn']")
#     search_button.click()
#
#     game_name_url_list.append(browser.current_url)
#
#     i+=1
# browser.close()
# browser.quit()
# print()