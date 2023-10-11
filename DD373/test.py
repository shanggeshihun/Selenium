# _*_coding:utf-8 _*_

#@Time      : 2021/12/22  9:53
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
html_queue = Queue()

start_url = 'https://game.dd373.com/y-0-1.html'
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=driver_path)

repeat_times = 0
while repeat_times <= 3:
    try:
        browser.get(start_url)
    except:
        repeat_times += 1
    else:
        break

# wait = WebDriverWait(browser, 3)
# ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '.game-list-ul.clearfix')))

# 所有游戏url列表(游戏url可能有重复)
game_href_list = []
for game in browser.find_elements_by_xpath("//ul[@class = 'game-list-ul clearfix']/li/a"):
    game_href_list.append((game.get_attribute('href'),game.find_element_by_tag_name('span').text))
for g in set(game_href_list):
    print(g)