# _*_coding:utf-8 _*_

# @Time      : 2021/12/23  21:09
# @Author    : An
# @File      : main_multi_threading_5173_webgame_all.py
# @Software  : PyCharm

"""
注意事项：
1）队列获取数据时，q.get(False)否则没有元素时会一直阻塞
"""

"""
一、从 http://www.5173.com/ 进入爬虫游戏（通过游戏首字母遍历所有游戏）
    一级页面 ：所有游戏
    二级页面 ：点击单个游戏进入的页面，该页面需要通过选择【商品类型】获取账号交易的网站地址
    三级页面 ：单个游戏账号交易的网站地址
    
    所有游戏列表作为爬虫队列
    每个游戏的每页页面数据作为解析队列
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading
from queue import Queue
from lxml import etree
import datetime,re

# 预警邮件提醒
# from WarningEmail import warning_email

import sys

sys.setrecursionlimit(20000)


class TradeDd373Thread(threading.Thread):
    def __init__(self, thread_id, game_url_queue, html_queue):
        threading.Thread.__init__(self)
        self.setName('Crawl' + self.name)
        driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
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

        self.game_url_queue = game_url_queue
        self.html_queue = html_queue

    def run(self):
        """
        :start_url:游戏的初始url
        :return:初始化browser对象
        """
        while GAME_QUEUE_NOT_EMPTY:
            try:
                start_url = self.game_url_queue.get(False)
                self.game_url_queue.task_done()
            except:
                pass
            else:
                self.game_account_page(start_url)
                self.check_next_page()
        self.browser.quit()

    def game_account_page(self, start_url):
        """
        :param start_url: 某游戏起始页面
        :return: 某游戏的交易账号页面
        """

        """
        Unable to locate element: {"method":"css selector","selector":"[class='list-panel select-type']"}
        """
        try_times = 0
        while try_times < 3:
            try:
                self.browser.get(start_url)
                time.sleep(3)
                fit_list = self.browser.find_element_by_class_name("fit-list")
                goods_select_value = fit_list.find_element_by_css_selector("[class='list-panel select-type']")
            except:
                self.browser.refresh()
                time.sleep(3)
                try_times += 1
            else:
                break

        if try_times == 3:
            return

        goods_select = goods_select_value.find_elements_by_xpath("./span")
        choice_list = []
        for choice in goods_select:
            choice_list.append(choice.text)
        if '帐号' in choice_list:
            return goods_select_value.find_element_by_link_text("帐号").click()

    def check_next_page(self):
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
                ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagesmvc')))
            except:
                self.browser.refresh()
                time.sleep(3)
                try_times += 1
            else:
                break
        if try_times == 3:
            return

        # 当前第N页(可能有验证码)
        while True:
            try:
                laypage_cur = int(
                    self.browser.find_element_by_xpath("//input[@id='_Pager_Ctrl0_pib']").get_attribute("value"))
            except Exception as e:
                print('【异常】手工处理:', e)
                time.sleep(180)
                self.browser.refresh()
            else:
                break

        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title
        print(threading.current_thread().name, '', cur_page_title, ' ', cur_page_url, ' 第 ', laypage_cur, '页列表')
        time.sleep(1)

        # 每个处理20页，等待30秒
        if laypage_cur % 20 == 0:
            time.sleep(30)

        # 每个处理70页，等待60秒
        if laypage_cur % 70 == 0:
            time.sleep(60)

        # 页面链接+页面page_source均写入队列
        self.html_queue.put((cur_page_url, self.browser.MUSIC_URL_QUEUE_NOT_EMPTY))

        laypage_main = self.browser.find_element_by_xpath("//tr[@class='page-list text-center']//label")

        # 查看 【下一页】是否存在（下一页是否在链接标签中）
        page_num_tag_list = laypage_main.find_elements_by_xpath('./a[@href]')
        page_name_list = [page.text for page in page_num_tag_list]

        if '下一页' in page_name_list:
            next_page = laypage_main.find_element_by_link_text('下一页')
            next_page.click()

            """
            点击下一页等待2秒，作3次尝试。
            第一次：如果等待后下一页页码比上一页大1，则加载完成，跳出尝试，否则再等待5秒
            第                                                                                   二次：如果第一次等待5秒后，仍没有加载到下一页，则刷新页面，并等待5秒
            第三次：仍没有加载完，则数据重复
            """
            time.sleep(2)
            # 确定有下一页时，点击后检查是否正常跳转到了新页面
            check_times = 0
            while check_times < 3:
                # 当前第N页
                next_page_num = int(
                    self.browser.find_element_by_xpath("//input[@id='_Pager_Ctrl0_pib']").get_attribute("value"))
                if next_page_num == laypage_cur + 1:
                    print('           【成功】加载下一页，尝试第{}次后'.format(check_times))
                    break
                else:
                    if check_times == 1:
                        self.browser.refresh()
                        print('           【刷新】页面，尝试第{}次后'.format(check_times))
                    time.sleep(5)
                    check_times += 1
            if check_times == 3:
                print('           【未知】加载下一页，尝试第{}次后加，等待下次尝试'.format(check_times))
            self.check_next_page()
        else:
            # 从起始页到最后一次页遍历完成
            # self.browser.close()
            return


class ParseTradeDd373Thread(threading.Thread):
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
                self.parse_next_page_detail(html)
        self.cur.close()
        self.con.close()
        print('关闭数据库连接')

    def parse_next_page_detail(self, html):
        """
        :param browser: 单个游戏页面的browser
        :return:
        """
        game_page_url = html[0]
        page_source = html[1]
        html = etree.HTML(MUSIC_URL_QUEUE_NOT_EMPTYce)
        goods_list_item = html.xpath("//table[@class = 'table table-striped good-list']/tbody/tr")

        print(threading.current_thread().name, ' 正在解析页面游戏链接：{0}'.format(game_page_url))

        item_count = 1
        for item_box in goods_list_item:

            try:
                title = item_box.xpath(".//p[@class='title']/a/text()")[0].strip().replace("\n", "")
            except:
                title = ''

            try:
                zone_name = item_box.xpath(
                    ".//span[@class='good-info']/p[contains(text(),'游戏区服')]/span/text()")[0].strip().replace("\n", "")
            except:
                zone_name = ''
            try:
                price = item_box.xpath(
                    ".//td[@class='orange']/text()")[0].strip().replace("\n", "")
            except:
                price = '100000000'

            try:
                server_protection = item_box.xpath(
                    ".//td[@class='serve']/p/text()")
                server_protection = '/'.join([s.replace('\n', '').strip() for s in server_protection])
            except Exception as e:
                server_protection = ''

            try:
                text_center = item_box.xpath(".//td[@class='text-center']/a/@onclick")[0]
                pattern = re.compile(r"'(.*?)'")
                info = pattern.findall(text_center)

                goods_code = info[0]
                goods_title = info[1]
                goods_type = info[2]
                goods_price = info[3]
                goods_game = info[4]
                goods_os = info[5]
            except:
                goods_code = ''
                goods_title = ''
                goods_type = ''
                goods_price = '100000000'
                goods_game = ''
                goods_os = ''

            game_name = zone_name.split('-')[0]

            etl_time = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime('%Y-%m-%d %H:%M:%S')

            item = {
                'game_page_url': game_page_url,
                'game_name': game_name,
                'zone_name': zone_name,
                'title': title,
                'price': float(price.replace("'",'')),
                'server_protection': server_protection,
                'goods_code': goods_code,
                'goods_title': goods_title,
                'goods_type': goods_type,
                'goods_price': float(goods_price.replace("'",'')),
                'goods_name': goods_game,
                'goods_os': goods_os,
                'etl_time': etl_time
            }

            filed_tuple = (
                'game_page_url', 'game_name', 'zone_name', 'title', 'price', 'server_protection', 'goods_code',
                'goods_title', 'goods_type', 'goods_price', 'goods_name', 'goods_os','etl_time')
            filed_values_tuple = tuple(item.values())
            self.insert_db(filed_tuple, filed_values_tuple)
            item_count += 1

    def insert_db(self, filed_tuple, filed_values_tuple):
        try:
            sql = "insert into trade_5173_mobilegame_result({})values{}".format(','.join(filed_tuple),
                                                                                filed_values_tuple)
            self.cur.execute(sql)
            self.cur.execute('commit')
        except Exception as e:
            print(e)


def game_start_url_list():
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

    repeat_times = 0
    while repeat_times <= 3:
        try:
            browser.get(start_url)
        except:
            repeat_times += 1
        else:
            break

    # wait = WebDriverWait(browser, 3)
    # ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'game-list-ul clearfix')))

    # netgame  netgame-hotspell
    # mobilegame mobilegame-hotspell
    # webgame webgame-hotspell
    mobilegame_bnt = browser.find_element_by_xpath("//li[@data-tab='mobilegame']")
    mobilegame_bnt.click()
    time.sleep(2)

    # 所有游戏url列表(游戏url可能有重复)
    game_href_list = []

    first_letter = browser.find_elements_by_xpath("//ul[@class='tab-letter clearfix']/li")

    for fl in first_letter:
        tmp_game_href_list = []
        if fl.get_attribute('class') == 'hot':
            continue

        fl.click()
        time.sleep(3)

        print("----------------------当前是首字母------------------------", fl.text)
        game_xpath_name = "//ul[@class='gamelist-ul clearfix mobilegame-{}']/li/a[@class='link-all']".format(fl.text)
        print(game_xpath_name)

        g = browser.find_elements_by_xpath(game_xpath_name)

        if not g:
            continue
        else:
            for game in g:
                tmp_game_href_list.append(game.get_attribute('href'))
                game_href_list.append(game.get_attribute('href'))
            print(tmp_game_href_list)
    browser.close()
    browser.quit()
    return game_href_list

GAME_QUEUE_NOT_EMPTY = True
HTML_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()


def main():
    # 游戏链接组成的队列
    game_url_queue = Queue()
    # 解析队列
    html_queue = Queue()

    with open("./mobilegame_info.txt", 'r', encoding='utf-8') as f:
        game_url_list = [line.split(',')[2].strip() for line in f.readlines()]

    game_href_list = game_url_list
    for game in set(game_href_list):
        # if game in ['https://www.dd373.com/s-eja7u2.html']:
        game_url_queue.put(game)

    trade_thread_name_list = ['trade' + str(i) for i in range(5)]
    trade_thread_list = []
    for thread_id in trade_thread_name_list:
        thread = TradeDd373Thread(thread_id, game_url_queue, html_queue)
        thread.start()
        trade_thread_list.append(thread)

    parse_thread_name_list = ['parse' + str(i) for i in range(10)]
    parse_thread_list = []
    for thread_id in parse_thread_name_list:
        thread = ParseTradeDd373Thread(thread_id, html_queue)
        thread.start()
        parse_thread_list.append(thread)

    while not game_url_queue.empty():
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


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
