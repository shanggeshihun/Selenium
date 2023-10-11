# _*_coding:utf-8 _*_

# @Time      : 2021/12/27  9:28
# @Author    : An
# @File      : main_multi_threading_pzds_all.py
# @Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading, json, re, datetime
from queue import Queue
from lxml import etree


class TradePzdsThread(threading.Thread):
    def __init__(self, thread_id, game_queue, html_queue):
        threading.Thread.__init__(self)
        self.setName('Crawl' + self.name)
        driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        # 使用开发者模式
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        self.game_queue = game_queue
        self.html_queue = html_queue

    def run(self):
        """
        :start_url:游戏的初始url
        :return:初始化browser对象
        """
        while GAME_QUEUE_NOT_EMPTY:
            try:
                thread_lock.acquire()
                game_id_name = self.game_queue.get(False)
                self.game_queue.task_done()
                thread_lock.release()

                start_url = self.get_the_game_dealt_accounts_url(game_id_name)
                self.get_page_source(start_url)
            except Exception as e:
                print('get_page_source(start_url) 异常', start_url)
                pass
            else:
                self.check_and_click_page()
        self.browser.quit()

    def get_the_game_dealt_accounts_url(self, game_id_name):
        game_deal_url = 'https://www.pzds.com/goodsList?gameId={0}&gameName={1}/'.format(game_id_name[0],
                                                                                         game_id_name[1])
        repeat_times = 0
        while repeat_times <= 3:
            try:
                self.browser.get(game_deal_url)
            except:
                repeat_times += 1
            else:
                break
        repeat_times = 0
        while repeat_times <= 3:
            self.browser.refresh()
            time.sleep(5)
            try:
                wait = WebDriverWait(self.browser, 3)
                ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'view-more')))
            except Exception as e:
                repeat_times += 1
                print('start_url:请求异常', game_deal_url)
                time.sleep(10)
            else:
                start_url = self.browser.find_element_by_xpath("//a[@class='view-more']").get_attribute('href')
                return start_url
                break
        if repeat_times == 3:
            return

    def get_page_source(self, start_url):
        """
        :param start_url:初始化页面（某游戏的交易账号的第一个页面）
        :return:
        """
        self.browser.get(start_url)

    def check_and_click_page(self):
        """
        :param browser:启动页面(点击某个游戏后首次跳转到的页面)
        :return:解析该页面后获取返回字段
        """

        # 多次尝试 减少timeout
        """
        ul = wait.until  raise TimeoutException(message, screen, stacktrace)
        """
        # 显式等待
        try_times = 0
        while try_times < 3:
            try:
                wait = WebDriverWait(self.browser, 5)
                ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-pagination__total')))
            except:
                self.browser.refresh()
                time.sleep(3)
                try_times += 1
            else:
                break
        if try_times == 3:
            return

        # # 当前第N页(可能有验证码)
        # while True:
        #     try:
        #         laypage_cur = int(
        #             self.browser.find_element_by_xpath("//input[@id='_Pager_Ctrl0_pib']").get_attribute("value"))
        #     except Exception as e:
        #         print('【异常】手工处理:', e)
        #         time.sleep(1)
        #         self.browser.refresh()
        #     else:
        #         break

        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title

        # 当前是第N页
        cur_page_number = self.browser.find_element_by_xpath("//ul[@class='el-pager']/li[@class='number active']").text
        cur_page_number = int(cur_page_number)

        # print(threading.current_thread().name, '', cur_page_title, ' ', cur_page_url, ' 第 ', cur_page_number, '页列表')
        print(threading.current_thread().name, '', cur_page_url, ' 第 ', cur_page_number, '页列表')
        time.sleep(1)

        # 每个处理20页，等待30秒
        if cur_page_number % 20 == 0:
            time.sleep(30)

        # 每个处理70页，等待60秒
        if cur_page_number % 70 == 0:
            time.sleep(60)

        # 页面链接+页面page_source均写入队列
        self.html_queue.put((cur_page_url, self.browser.page_source))

        # 总页面数
        page_number_element_list = self.browser.find_elements_by_xpath("//ul[@class='el-pager']/li")
        page_number_list = [int(ele.text) for ele in page_number_element_list if len(ele.text)]
        max_number = max(page_number_list)

        # print('cur_page_number:{0},max_number:{1}'.format(cur_page_number, max_number))
        if cur_page_number < max_number:
            btn_next = self.browser.find_element_by_xpath("//button[@class='btn-next']")
            btn_next.click()

            time.sleep(3)
            self.check_and_click_page()
        else:
            return


class ParseTradePzdsThread(threading.Thread):
    def __init__(self, thread_id, html_queue):
        """
        :param thread_id: 爬虫线程
        :param html_queue: 页面链接 + 页面page_source 为元组元素的队列
        """
        threading.Thread.__init__(self)
        self.setName('Parse' + self.name)

        self.html_queue = html_queue
        self.con = pymysql.connect(
            host='localhost',
            user='root',
            passwd='052206',
            port=3306,
            db='test'
        )
        self.cur = self.con.cursor()  # 数据库游标
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')

    def run(self):
        while HTML_QUEUE_NOT_EMPTY:
            try:
                html = self.html_queue.get(False)
                self.html_queue.task_done()
            except:
                pass
            else:
                self.parse_page_detail(html)
        self.cur.close()
        self.con.close()
        print('关闭数据库连接')

    def parse_page_detail(self, html):
        """
        :param browser: 单个游戏页面的browser
        :return:
        """
        game_page_url = html[0]
        game_id = int(re.findall('gameId=(\d+)&', game_page_url)[0])
        game_name = game_id_name_dict[game_id]

        print(threading.current_thread().name, ' 正在解析页面游戏', game_name, game_page_url)

        page_source = html[1]

        html = etree.HTML(page_source)

        item_list = html.xpath("//div[@class='goods-more-item vue-click-mask']")

        item_count = 0
        for item in item_list:
            try:
                goods_title = item.xpath(".//div[@class='goods-title text-333']/span/text()")[0]
                p = re.compile('(\w+)\s?号',re.A)
                goods_code = p.findall(goods_title)[0]
            except:
                goods_title = ''
                goods_code = ''

            try:
                goods_serve = item.xpath(".//div[@class='goods-server text-777 f12']/span/text()")[0]
            except:
                goods_serve = ''

            try:
                goods_publish_time = item.xpath(".//div[@class='mt-10 text-777 f12']/span[1]/text()")[0].replace(
                    '发布时间：', '')
            except:
                goods_publish_time = ''

            try:
                goods_dealt_time = item.xpath(".//div[@class='mt-10 text-777 f12']/span[2]/text()")[0].replace('成交时间：',
                                                                                                               '')
            except:
                goods_dealt_time = ''

            try:
                goods_price = item.xpath(".//span[@class='f18']/text()")[0]
            except:
                goods_price = 100000000

            try:
                goods_deal_status = item.xpath(".//div[@class='vue-hover-mask_center-box']/p/text()")[0]
            except:
                goods_deal_status = ''

            etl_time = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime('%Y-%m-%d %H:%M:%S')

            item_dict = {
                'game_page_url': game_page_url,
                'game_id': game_id,
                'game_name': game_name,
                'goods_code': goods_code,
                'goods_title': goods_title,
                'goods_serve': goods_serve,
                'goods_publish_time': goods_publish_time,
                'goods_dealt_time': goods_dealt_time,
                'goods_price': goods_price,
                'goods_deal_status': goods_deal_status,
                'etl_time': etl_time
            }

            filed_tuple = (
                'game_page_url', 'game_id', 'game_name', 'goods_code', 'goods_title', 'goods_serve',
                'goods_publish_time',
                'goods_dealt_time', 'goods_price', 'goods_deal_status', 'etl_time')
            filed_values_tuple = tuple(item_dict.values())
            self.insert_db(filed_tuple, filed_values_tuple)
            item_count += 1

    def insert_db(self, filed_tuple, filed_values_tuple):
        try:
            sql = "insert into pzds({})values{}".format(','.join(filed_tuple),
                                                        filed_values_tuple)
            self.cur.execute(sql)
            self.cur.execute('commit')
        except Exception as e:
            print(e)


def main():
    # 游戏链接组成的队列
    game_queue = Queue()

    # 解析队列
    html_queue = Queue()

    for id, game in game_id_name_dict.items():
        game_queue.put((id, game))

    trade_thread_name_list = ['trade' + str(i) for i in range(4)]
    trade_thread_list = []
    for thread_id in trade_thread_name_list:
        thread = TradePzdsThread(thread_id, game_queue, html_queue)
        thread.start()
        trade_thread_list.append(thread)

    parse_thread_name_list = ['parse' + str(i) for i in range(5)]
    parse_thread_list = []
    for thread_id in parse_thread_name_list:
        thread = ParseTradePzdsThread(thread_id, html_queue)
        thread.start()
        parse_thread_list.append(thread)

    while not game_queue.empty():
        pass
    global GAME_QUEUE_NOT_EMPTY
    GAME_QUEUE_NOT_EMPTY = False

    for t in trade_thread_list:
        t.join()
    print('爬虫程序已结束')

    while not html_queue.empty():
        pass
    global HTML_QUEUE_NOT_EMPTY
    HTML_QUEUE_NOT_EMPTY = False
    for t in parse_thread_list:
        t.join()
    print('解析程序已经结束')


GAME_QUEUE_NOT_EMPTY = True
HTML_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()

with open('./gameid_gamename.json', 'r') as f:
    gameid_gamename_list = json.load(f)

game_id_name_dict = {}
for game in gameid_gamename_list:
    game_id_name_dict[int(game['id'])] = game['name']

if __name__ == '__main__':
    main()
    # while True:
    #     today_hour = (datetime.datetime.now()).strftime('%H:%M:%S')  # 今日日期小时
    #     if today_hour == '09:00:00':
    #         start_time = time.time()
    #         main()
    #         print(time.time() - start_time)