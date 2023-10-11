# _*_coding:utf-8 _*_

# @Time     :2023/8/13 21:37
# @Author   :anliu
# @File     :download_by_music_name.py
# @Theme    :PyCharm

import sys
import requests
from selenium import webdriver
import time
# from lxml import etree
# from fake_useragent import UserAgent
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

sys.setrecursionlimit(100000)
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"

home_page_url = 'https://www.kugou.com/'

driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"


def  search_music(music_name):
    '''
    :param music_name:搜索歌曲名称
    :return: 返回歌曲下载链接列表
    '''
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

    browser.get(home_page_url)
    time.sleep(1)

    current_window, current_url = browser.current_window_handle, browser.current_url
    print('查询页面-窗口信息：', current_window)
    print('查询页面-当前窗口URL:', current_url)

    # 输入歌名
    browser.find_element_by_xpath('//div/input[@type="text"]').send_keys(music_name)
    time.sleep(3)
    # 提交查询
    browser.find_element_by_xpath('//div[contains(@class,"cmhead1_d8")]').click()
    time.sleep(3)

    current_window, current_url = browser.current_window_handle, browser.current_url
    print('提交查询返回页面-窗口信息：', current_window)
    print('提交查询返回页面-当前窗口URL:', current_url)

    # 获取提交歌名的播放页面
    browser.find_element_by_xpath('//div[@class="song_list"]//ul/li[1]/div/a[@class="song_name"]').click()
    time.sleep(3)

    # 获取所有窗口句柄列表
    handles = browser.window_handles
    # 切到新窗口
    new_window_handle = handles[-1]
    browser.switch_to.window(new_window_handle)

    current_window, current_url = browser.current_window_handle, browser.current_url
    print('播放页面-窗口信息：', current_window)
    print('播放页面-当前窗口URL:', current_url)


    mp3_url = browser.find_element_by_xpath('//audio[@class="music" and @id = "myAudio"]').get_attribute('src')
    print(mp3_url)

    browser.quit()
    browser.close()
    browser.service.stop()
    return mp3_url

def download_music(music_name,mp3_url):
    response = requests.get(url=mp3_url)
    if response.status_code == 200:
        with open('{}.mp3'.format(music_name), "wb") as fp:
            fp.write(response.content)
        print("下载完成")
    else:
        print('无法下载')
if __name__ == '__main__':
    music_name = '最熟悉的陌生人'
    mp3_url = search_music(music_name)
    if mp3_url != '':
        download_music(music_name, mp3_url)
