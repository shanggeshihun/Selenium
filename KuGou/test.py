# _*_coding:utf-8 _*_

# @Time     :2023/8/13 21:37
# @Author   :anliu
# @File     :test.py
# @Theme    :PyCharm

import sys
import requests
from selenium import webdriver
import time
# from lxml import etree
# from fake_useragent import UserAgent
import os
from selenium.webdriver.chrome.options import Options

sys.setrecursionlimit(100000)
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"

# def music_parse():
#     if not os.path.exists('./音乐'):
#         os.mkdir("音乐")
#         url=input('请输入歌曲地址')
#         wb=webdriver.Chrome(executable_path="./chromedriver.exe",options=chrome_options)
#         wb.get(url=url)
#         data=wb.page_source
#         wb.quit()
#         tree=etree.HTML(data)
#         music=tree.xpath('//*[@class="music"]/@src')[0]
#         musicname="./音乐/"+tree.xpath('//*[@class="audioName"]/@title')[0]+".mp3"
#         return music,musicname
#
# def music_download(music,musicname):
#     response=requests.get(url=music,headers=headers).content
#     with open(musicname,"wb") as fp:
#         fp.write(response)
#         print("下载完成")

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
    # 输入歌名
    browser.find_element_by_xpath('//div/input[@type="text"]').send_keys(music_name)
    time.sleep(1)
    # 提交查询
    browser.find_element_by_xpath('//div[contains(@class,"cmhead1_d8")]').click()
    time.sleep(1)
    # 获取提交歌名的播放页面
    browser.find_element_by_xpath('//div[@class="song_list"]//ul/li[1]/div/a[@class="song_name"]').click()

    time.sleep(1)

    current_window, current_url = browser.current_window_handle, browser.current_url
    print('当前窗口信息：', current_window)
    print('当前窗口URL:', current_url)

    # 切到新窗口
    handles = browser.window_handles
    print(len(handles),handles)
    browser.switch_to.window(handles[0])

    # 获取MP3链接

    print('当前窗口信息：', current_window)
    print('当前窗口URL:', current_url)

    mp3_url = ''
    mp3_url = browser.find_element_by_xpath('//audio[@class="music" and @id = "myAudio"]/@src')

    browser.close()
    browser.service.stop()
    return mp3_url

def download_music(mp3_url):
    response = requests.get(url=mp3_url).content
    with open(mp3_url,"wb") as fp:
        fp.write(response)
        print("下载完成")

if __name__ == '__main__':
    mp3_url = search_music('后来')
    if mp3_url != '':
        download_music(mp3_url)
