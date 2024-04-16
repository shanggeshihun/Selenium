# _*_coding:utf-8 _*_

# @Time     :2023/11/19 15:02
# @Author   :anliu
# @File     :download_m3u8_to_mp4_multi_threading.py
# @Theme    :PyCharm

"""
网站首页 home_url = 'https://www.vvvdj.com/'
起始页：网站首页&流行金曲&国语&全部&年度下载榜 start_url = 'https://www.vvvdj.com/sort/c2/4-5-0-7-1.html'
起始页：网站首页&发烧经典&国语&全部&年度下热播榜 start_url = 'https://www.vvvdj.com/sort/c2/5-5-0-6-1.html'
起始页：网站首页&流行金曲&全部&全部&年度下热播榜 start_url = 'https://www.vvvdj.com/sort/c2/4-0-0-6-1.html'
起始页：网站首页&发烧经典&国语&全部&年度下热播榜 start_url = 'https://www.vvvdj.com/sort/c2/5-5-0-6-1.html'
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading, json, os
from queue import Queue
from lxml import etree

import sys
sys.setrecursionlimit(20000)

HOME_URL = 'https://www.vvvdj.com/'
START_URL = 'https://www.vvvdj.com/sort/c2/4-0-0-6-1.html'
DRIVER_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"

CAPS = {
    "browserName": "chrome",
    'loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
}

M3U8_DOWNLOAD_DIR = './m3u8'
FFMPEG_PATH = r"D:\ffmpeg\bin\ffmpeg.exe"

# 名称及url初始化
TITLE_LIST, HREF_LIST = [], []



# 获取歌曲播放页面URL列表
class MusicEntranceUrl():
    def __init__(self):
        # 使用开发者模式
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(desired_capabilities=CAPS, executable_path=DRIVER_PATH, options=self.options)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.browser.get(START_URL)

    def get_music_entrance_url(self):

        tbody_xpath = '//div[@class="sort_list_left_ct"]/table/tbody'
        # 隐式等待列表出现
        i = 0
        while True:
            i += 1
            try:
                input_ele = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, tbody_xpath + '/tr[1]'))
                )
            except Exception as e:
                print('未加载到列表:', e)
                return None
            else:
                page_source = self.browser.page_source
            html = etree.HTML(page_source)
            tag_tbody = html.xpath(tbody_xpath)[0]
            tag_a_list = tag_tbody.xpath('./tr/td/div/li/a')

            for tag_a in tag_a_list:
                global TITLE_LIST
                TITLE_LIST.append(tag_a.xpath('./@title')[0])
                global HREF_LIST
                HREF_LIST.append(HOME_URL + tag_a.xpath('./@href')[0])

            # b_num 分别对应<<  <  >
            page_switch_xpath = "//div[@class='list_split_page']/form/li[@class='b']/a/text()"
            switch_list = html.xpath(page_switch_xpath)
            switch_list = [s.strip() for s in switch_list]

            if '>' not in switch_list:
                self.browser.quit()
                break
            next_ele = self.browser.find_element_by_xpath("//div[@class='list_split_page']/form/li[@class='b']/a[contains(text(),'>')]")
            next_ele.click()

            if i >=6:
                self.browser.quit()
                break

ENTRANCE_QUEUE_NOT_EMPTY = True
M3U8_URL_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()
thread_write_lock = threading.Lock()

class ParseToM3u8Thread(threading.Thread):
    def __init__(self, thread_id, entrance_url_queue, m3u8_url_queue):
        '''
        :param thread_id:
        :param entrance_url_queue: (名称 title,入口url href)作为元素的队列
        :param m3u8_url_queue:(名称 title,m3u8_url)作为元素的队列
        '''
        threading.Thread.__init__(self)
        self.setName('Crawl' + self.name)
        # 使用开发者模式
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(desired_capabilities=CAPS, executable_path=DRIVER_PATH, options=self.options)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        self.entrance_url_queue = entrance_url_queue
        self.m3u8_url_queue = m3u8_url_queue

    def run(self):
        print('当前线程',threading.current_thread().name)
        while ENTRANCE_QUEUE_NOT_EMPTY:
            try:
                entrance_url = self.entrance_url_queue.get(False)
                self.entrance_url_queue.task_done()
            except:
                pass
            else:
                print('当前线程', threading.current_thread().name, entrance_url)
                self.search_m3u8(entrance_url)

        if self.browser:
            return

    def search_m3u8(self, entrance_url):
        '''
        搜索歌曲名称
        :param entrance_url:歌曲播放页面 (title,href)
        :return: 返回歌曲下载链接 (title,m3u8)
        '''
        time.sleep(2)
        try:
            title, href = entrance_url[0], entrance_url[1]
            self.browser.get(href)
        except Exception as e:
            print(f'{entrance_url} 入口页面访问失败', e)
            return None

        # 获取Network数据
        performance_log = self.browser.get_log('performance')
        for packet in performance_log:
            message = json.loads(packet.get('message')).get('message')
            if message.get('method') != 'Network.responseReceived':
                continue
                
            packet_type = message.get('params').get('response').get('mimeType')
            types = [
                'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif','image/jpeg', 'image/x-icon', 'application/octet-stream'
            ]
            if packet_type in types:
                continue
            m3u8_url = message.get('params').get('response').get('url')  # 获取 该请求  url
            if 'm3u8' in m3u8_url:
                self.m3u8_url_queue.put((title, m3u8_url))
                break

class DownloadM3u8Thread(threading.Thread):
    def __init__(self, thread_id, m3u8_url_queue):
        threading.Thread.__init__(self)
        self.setName('Download' + self.name)
        self.m3u8_url_queue = m3u8_url_queue

    def run(self):
        print('当前线程',threading.current_thread().name)
        while M3U8_URL_QUEUE_NOT_EMPTY:
            time.sleep(2)
            try:
                m3u8_url = self.m3u8_url_queue.get(False)
                self.m3u8_url_queue.task_done()
            except:
                pass
            else:
                print('当前线程', threading.current_thread().name, m3u8_url[0])
                self.download_music(m3u8_url[0], m3u8_url[1])

    def download_music(self, title, m3u8_url):
        try:
            print(f'{FFMPEG_PATH} -allowed_extensions ALL -protocol_whitelist "file,http,crypto,https,tcp,tls" -i {m3u8_url}   {M3U8_DOWNLOAD_DIR}/{title}.mp4')
            os.system(f'{FFMPEG_PATH} -allowed_extensions ALL -protocol_whitelist "file,http,crypto,https,tcp,tls" -i {m3u8_url}   {M3U8_DOWNLOAD_DIR}/{title}.mp4')
        except Exception as e:
            print(f'{title} 下载失败', e)
        else:
            print(f'{title} 下载成功')

def main():
    m = MusicEntranceUrl()
    m.get_music_entrance_url()

    # 播放url队列
    entrance_url_queue = Queue()
    # 下载m3u8队列
    m3u8_url_queue = Queue()

    for idx, title in enumerate(TITLE_LIST):
        href = HREF_LIST[idx]
        entrance_url_queue.put((title, href))

    entrance_thread_name_list = ['entrance_thread_' + str(i) for i in range(4)]
    entrance_thread_list = []
    for thread_id in entrance_thread_name_list:
        thread = ParseToM3u8Thread(thread_id, entrance_url_queue, m3u8_url_queue)
        thread.start()
        entrance_thread_list.append(thread)

    download_thread_name_list = ['download_thread_' + str(i) for i in range(6)]
    download_thread_list = []
     # 如果 entrance_url_queue 为空，采集线程退出循环
    global ENTRANCE_QUEUE_NOT_EMPTY
    ENTRANCE_QUEUE_NOT_EMPTY = False
    print("\nentrance_url_queue 为空")

    # 让抓取主线程进入阻塞状态，等待子线程执行完毕再退出
    for t in entrance_thread_list:
        t.join()
    print('\n爬虫程序已结束')


    # 如果 download_thread_list 为空，下载线程退出循环
    while not m3u8_url_queue.empty():
        pass
    global M3U8_URL_QUEUE_NOT_EMPTY
    M3U8_URL_QUEUE_NOT_EMPTY = False

    # 让下载主线程进入阻塞状态，等待子线程执行完毕再退出
    for t in download_thread_list:
        t.join()
    print('\n下载程序已经结束')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
