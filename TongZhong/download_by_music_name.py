# _*_coding:utf-8 _*_

# @Time     :2023/8/13 21:37
# @Author   :anliu
# @File     :download_by_music_name.py
# @Theme    :PyCharm

import sys, warnings
import requests
from selenium import webdriver
import time
# from lxml import etree
# from fake_useragent import UserAgent
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

# 关闭特定的警告
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"

home_page_url = 'https://tonzhon.com/music_for_commercial_use'




def search_music(music_name):
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
    time.sleep(2)

    current_window, current_url = browser.current_window_handle, browser.current_url
    # print('查询页面-窗口信息：', current_window)
    # print('查询页面-当前窗口URL:', current_url)

    # 输入歌名
    try:
        browser.find_element_by_xpath('//input[@type="text"]').send_keys(music_name)
    except Exception as e:
        print('输入歌名 模拟异常')
        browser.quit()
        return
    else:
        time.sleep(3)

    # 提交查询
    try:
        browser.find_element_by_xpath('//button[contains(@type,"button")]').click()
    except Exception as e:
        print('提交查询 模拟异常')
        browser.quit()
        return
    else:
        time.sleep(5)

    current_window, current_url = browser.current_window_handle, browser.current_url
    # print('提交查询返回页面-窗口信息：', current_window)
    # print('提交查询返回页面-当前窗口URL:', current_url)

    # 点击播放按钮
    try:
        browser.find_element_by_xpath(
        '//div[@class="masonry"]/div[contains(@class,"card search-result")][3]//li[contains(@class,"song-item")]//div[@class="ant-row ant-row-middle css-tx6cnl"]/div/div/div[@class="ant-space-item"]'
        ).click()
    except Exception as e:
        print('点击播放 模拟异常')
        browser.quit()
        return
    else:
        time.sleep(5)

    current_window, current_url = browser.current_window_handle, browser.current_url
    # print('播放页面-窗口信息：', current_window)
    # print('播放页面-当前窗口URL:', current_url)

    try:
        mp3_url = browser.find_element_by_xpath('//div[@id="player"]/audio').get_attribute('src')
    except Exception as e:
        print('获取MP3 失败')
        return
    else:
        browser.quit()
        return mp3_url


def download_music(music_name, mp3_url):
    response = requests.get(url=mp3_url, verify=False)
    if response.status_code == 200:
        with open(r'./musics/{}.mp3'.format(music_name), "wb") as fp:
            fp.write(response.content)
        return True
    else:
        return False


if __name__ == '__main__':
    with open(r'./music_list.txt', mode='r', encoding='utf-8', ) as f:
        musics_list = f.readlines()

    for music in musics_list:
        music_name = music.strip()
        print('----------------《{}》正在下载----------------'.format(music_name))
        # 初始化下载状态
        is_download = False
        for _ in range(2):
            mp3_url = search_music(music_name)
            if not mp3_url:
                continue
                time.sleep(2)
            else:
                is_download = download_music(music_name, mp3_url)

            if is_download:
                break
        if not is_download:
            print('\t下载失败')