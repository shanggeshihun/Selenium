# _*_coding:utf-8 _*_

# @Time     :2023/11/15 7:24
# @Author   :anliu
# @File     :download_by_music_name.py
# @Theme    :注意 最后会自动退出线程，因此不需要在脚本中体现 browser.quit()

import requests, time, os, warnings, threading
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue

# 关闭特定的警告
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# 常量定义
DRIVER_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
HOME_PAGE_URL = 'https://tonzhon.com/music_for_commercial_use'
MUSIC_LIST_FILE_PATH = r'./music_list.txt'
MUSIC_DOWNLOAD_DIR = './musics'

MUSIC_QUEUE_NOT_EMPTY = True
MUSIC_URL_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()
thread_write_lock = threading.Lock()

class ZhongTongMp3UrlThread(threading.Thread):
    def __init__(self, thread_id, music_name_queue, music_url_queue):
        threading.Thread.__init__(self)
        self.setName('Crawl' + self.name)
        # 使用开发者模式
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        self.music_name_queue = music_name_queue
        self.music_url_queue = music_url_queue

    def run(self):
        print('当前线程',threading.current_thread().name)
        while MUSIC_QUEUE_NOT_EMPTY:
            try:
                music_name = self.music_name_queue.get(False)
                self.music_name_queue.task_done()
            except:
                pass
            else:
                print('当前线程', threading.current_thread().name, music_name)
                self.search_music(music_name)

        if self.browser:
            # self.browser.quit()
            return

    def search_music(self, music_name):
        '''
        搜索歌曲名称
        :param music_name:搜索歌曲名称
        :return: 返回歌曲下载链接列表
        '''

        try:
            self.browser.get(HOME_PAGE_URL)
        except Exception as e:
            print(f'{music_name} 主页访问失败', e)
            return None

        # 输入歌名
        try:
            input_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
            )
            input_element.send_keys(music_name)
        except Exception as e:
            print('输入歌名失败:', e)
            # self.browser.quit()
            return None

        # 提交查询
        try:
            submit_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@type,"button")]'))
            )
            submit_button.click()
        except Exception as e:
            print('提交查询失败:', e)
            # self.browser.quit()
            return None

        time.sleep(5)
        # 点击播放按钮
        try:
            play_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="masonry"]/div[contains(@class,"card search-result")][3]//li[contains(@class,"song-item")]//div[@class="ant-row ant-row-middle css-tx6cnl"]/div/div/div[@class="ant-space-item"]'))
            )
        except Exception as e:
            try:
                self.browser.execute_script("window.scrollBy(0, 500);")
                play_button = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//div[@class="masonry"]/div[contains(@class,"card search-result")][4]//li[contains(@class,"song-item")]//div[@class="ant-row ant-row-middle css-tx6cnl"]/div/div/div[@class="ant-space-item"]'))
                )
            except Exception as e:
                print('\t点击播放失败:', e)
                # self.browser.quit()
                return None
            else:
                play_button.click()
        else:
            play_button.click()

        time.sleep(3)
        # 获取MP3链接
        try:
            mp3_url = self.browser.find_element_by_xpath('//div[@id="player"]/audio').get_attribute('src')
        except Exception as e:
            print('\t获取MP3链接失败:', e)
            # self.browser.quit()
            return None
        else:
            # self.browser.quit()
            self.music_url_queue.put((music_name, mp3_url))

class DownloadMusicThread(threading.Thread):
    def __init__(self, thread_id, music_url_queue):
        threading.Thread.__init__(self)
        self.setName('Parse' + self.name)
        self.music_url_queue = music_url_queue

    def run(self):
        print('当前线程',threading.current_thread().name)
        while MUSIC_URL_QUEUE_NOT_EMPTY:
            try:
                music_url = self.music_url_queue.get(False)
                self.music_url_queue.task_done()
            except:
                pass
            else:
                print('当前线程', threading.current_thread().name, music_url[0])
                self.download_music(music_url[0], music_url[1])

    def download_music(self, music_name, mp3_url):
        response = requests.get(url=mp3_url)
        if response.status_code == 200:
            with open(os.path.join(MUSIC_DOWNLOAD_DIR, f'{music_name}.mp3'), "wb") as fp:
                fp.write(response.content)
                print(f'{music_name} 下载成功')
        else:
            print(f'{music_name} 下载失败')



def main():
    # 音乐名称队列
    music_name_queue = Queue()
    # 下载链接对接
    music_url_queue = Queue()

    with open(MUSIC_LIST_FILE_PATH, mode='r', encoding='utf-8') as f:
        music_list = f.readlines()

    for music in music_list:
        music_name_queue.put(music.strip())

    music_thread_name_list = ['music_thread_' + str(i) for i in range(4)]
    music_thread_list = []
    for thread_id in music_thread_name_list:
        thread = ZhongTongMp3UrlThread(thread_id, music_name_queue, music_url_queue)
        thread.start()
        music_thread_list.append(thread)

    download_thread_name_list = ['download_thread_' + str(i) for i in range(4)]
    download_thread_list = []
    for thread_id in download_thread_name_list:
        thread = DownloadMusicThread(thread_id, music_url_queue)
        thread.start()
        download_thread_list.append(thread)


    while not music_name_queue.empty():
        pass
    # 如果 music_name_queue 为空，采集线程退出循环
    global MUSIC_QUEUE_NOT_EMPTY
    MUSIC_QUEUE_NOT_EMPTY = False
    print("\nmusic_name_queue 为空")

    # 让抓取主线程进入阻塞状态，等待子线程执行完毕再退出
    for t in music_thread_list:
        t.join()
    print('\n爬虫程序已结束')


    # 如果 music_url_queue 为空，下载线程退出循环
    while not music_url_queue.empty():
        pass
    global MUSIC_URL_QUEUE_NOT_EMPTY
    MUSIC_URL_QUEUE_NOT_EMPTY = False

    # 让下载主线程进入阻塞状态，等待子线程执行完毕再退出
    for t in download_thread_list:
        t.join()
    print('\n下载程序已经结束')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)