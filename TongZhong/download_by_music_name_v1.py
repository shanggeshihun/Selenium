# _*_coding:utf-8 _*_

# @Time     :2023/11/15 7:24
# @Author   :anliu
# @File     :download_by_music_name.py
# @Theme    :PyCharm

import requests
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 常量定义
DRIVER_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
HOME_PAGE_URL = 'https://tonzhon.com/music_for_commercial_use'
MUSIC_LIST_FILE_PATH = r'./music_list.txt'
MUSIC_DOWNLOAD_DIR = './musics'

# 配置ChromeDriver选项
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 初始化webdriver
browser = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

def search_music(music_name):
    '''
    搜索歌曲名称
    :param music_name:搜索歌曲名称
    :return: 返回歌曲下载链接列表
    '''
    browser.get(HOME_PAGE_URL)
    # 输入歌名
    try:
        input_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
        )
        input_element.send_keys(music_name)
    except Exception as e:
        print('输入歌名失败:', e)
        return None

    # 提交查询
    try:
        submit_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@type,"button")]'))
        )
        submit_button.click()
    except Exception as e:
        print('提交查询失败:', e)
        return None

    # 等待页面加载
    time.sleep(5)

    # 点击播放按钮
    try:
        play_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="masonry"]/div[contains(@class,"card search-result")][3]//li[contains(@class,"song-item")]//div[@class="ant-row ant-row-middle css-tx6cnl"]/div/div/div[@class="ant-space-item"]'))
        )
        play_button.click()
    except Exception as e:
        print('点击播放失败:', e)
        return None

    # 等待页面加载
    time.sleep(5)

    # 获取MP3链接
    try:
        mp3_url = browser.find_element_by_xpath('//div[@id="player"]/audio').get_attribute('src')
    except Exception as e:
        print('获取MP3链接失败:', e)
        return None

    return mp3_url

def download_music(music_name, mp3_url):
    response = requests.get(url=mp3_url, verify=False)
    if response.status_code == 200:
        with open(os.path.join(MUSIC_DOWNLOAD_DIR, f'{music_name}.mp3'), "wb") as fp:
            fp.write(response.content)
        return True
    else:
        return False

if __name__ == '__main__':
    with open(MUSIC_LIST_FILE_PATH, mode='r', encoding='utf-8') as f:
        musics_list = f.readlines()

    for music in musics_list:
        music_name = music.strip()
        print(f'----------------《{music_name}》正在下载----------------')
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

    browser.quit()  # 退出浏览器