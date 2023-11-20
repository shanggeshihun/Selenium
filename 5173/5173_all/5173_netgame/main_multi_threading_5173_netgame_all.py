# _*_coding:utf-8 _*_

# @Time      : 2021/12/29  17:29
# @Author    : An
# @File      : main_multi_threading_5173_webgame_all.py
# @Software  : PyCharm

"""
注意事项：
1）队列获取数据时，q.get(False)否则没有元素时会一直阻塞

备注：
1）所有的游戏都保存到txt
2）缩短等待时长，每处理20页等待10s，每处理70等待30s
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
import time, csv, pymysql, threading,datetime,re
from queue import Queue
from lxml import etree

# 预警邮件提醒
from WarningEmail import warning_email

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
                thread_lock.acquire()
                start_url = self.game_url_queue.get(False)
                self.game_url_queue.task_done()
                thread_lock.release()
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
                goods_select_value = self.browser.find_element_by_xpath("//dl[@id='dlGameCategory']")
            except:
                self.browser.refresh()
                time.sleep(3)
                try_times += 1
            else:
                break

        if try_times == 3:
            return

        goods_select = goods_select_value.find_elements_by_xpath("./dt/a")
        choice_list = []
        for choice in goods_select:
            choice_list.append(choice.text)
        if '游戏帐号' in choice_list:
            return goods_select_value.find_element_by_link_text("游戏帐号").click()

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
                ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
            except:
                self.browser.refresh()
                time.sleep(3)
                try_times += 1
            else:
                break
        if try_times == 3:
            return

        # 当前第N页(可能有验证码)
        # 只有一页的账号交易列表，没有显示页码栏
        try_times = 0
        # 初始化当前页码
        laypage_cur = 1
        while try_times < 3:
            try:
                laypage_cur = int(
                    self.browser.find_element_by_xpath("//div[@class='page-list']/span[@class='current']").text)
            except Exception as e:
                if try_times == 2:
                    print('【异常】手工处理:', self.browser.current_url)
                try_times += 1
                time.sleep(2)
                self.browser.refresh()
            else:
                break

        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title
        print(threading.current_thread().name, '', cur_page_title, ' ', cur_page_url, ' 第 ', laypage_cur, '页列表')

        call_threading_info = threading.current_thread().name + " " + cur_page_title + " " + cur_page_url + " 第 " + str(
            laypage_cur) + "页列表"

        self.writelines(call_threading_info)

        time.sleep(1)

        # 每个处理20页，等待30秒
        if laypage_cur % 20 == 0:
            time.sleep(10)

        # 每个处理70页，等待60秒
        if laypage_cur % 70 == 0:
            time.sleep(20)

        # 页面链接+页面MUSIC_URL_QUEUE_NOT_EMPTYce均写入队列
        self.html_queue.put((cur_page_url, self.browser.page_source))

        # 只有一页的账号交易列表，没有显示页码栏
        try:
            total_page = int(
            self.browser.find_element_by_xpath("//div[@class='page-list']/span[@class='page_total']").text.replace("共","").replace("页", ""))
        except:
            total_page =1

        if laypage_cur < total_page:
            next_page_num = laypage_cur + 1

            next_page_xpath = "//div[@class='page-list']/a[@rel='{}' and @class='page_no']".format(next_page_num)
            print(next_page_xpath)
            next_page = self.browser.find_element_by_xpath(next_page_xpath)

            next_page.send_keys("Keys.SPACE")
            next_page.click()
            # self.browser.execute_script("arguments[0].click();", next_page)

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
                    int(
                        self.browser.find_element_by_xpath("//div[@class='page-list']/span[@class='current']").text))
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

    def writelines(self, write_info):
        thread_write_lock.acquire()
        with open("./webgame_threading_info.txt", "a+", encoding="utf-8") as f:
            f.write(write_info)
            f.write("\n")
        thread_write_lock.release()


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
        html = etree.HTML(page_source)
        goods_list_item = html.xpath("//div[@class = 'pdlistbox']/div[@class='sin_pdlbox']")

        print(threading.current_thread().name, ' 正在解析页面游戏链接：{0}'.format(game_page_url))
        item_count = 1
        for item_box in goods_list_item:

            try:
                title = item_box.xpath("./ul[@class='pdlist_info']/li[@class='tt']//a[@href and @onclick]/text()")[
                    0].strip().replace("\n", "")
            except:
                title = ''

            try:
                marchant_credit = item_box.xpath("./ul[@class='pdlist_info']/li[@class='credit']/a/@title")[
                    0].strip().replace("\n", "")
            except:
                marchant_credit = ''

            try:
                marchant_credit_icon = item_box.xpath("./ul[@class='pdlist_info']/li[@class='credit']/a/span/@class")[
                    0].strip().replace("\n", "")
            except:
                marchant_credit_icon = ''

            try:
                zone_name = item_box.xpath("./ul[@class='pdlist_info']/li[contains(text(),'游戏')]/a")
                zone_name = '/'.join([g.xpath("./text()")[0].strip().replace("\n", "") for g in zone_name])
            except:
                zone_name = ''

            try:
                price = item_box.xpath(
                    "./ul[@class='pdlist_price']/li[@class='pr']/strong/text()")[0].strip().replace("\n", "")
            except:
                price = ''

            try:
                publish_time = item_box.xpath(
                    "./ul[@class='pdlist_num']/li/text()")[0].strip().replace("\n", "")
            except:
                publish_time = ''

            try:
                ensure = item_box.xpath(
                    "./ul[@class='pdlist_ensure']/li/a/span/text()")
                ensure = '/'.join(ensure)
            except:
                ensure = ''

            try:
                text_center = item_box.xpath(
                    "./ul[@class='pdlist_way']/li[@class='goto_buy']/a/@onclick")[0]
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

            game_name = zone_name.split('/')[0]

            etl_time = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime('%Y-%m-%d %H:%M:%S')

            item = {
                'game_page_url': game_page_url,
                'game_name': game_name,
                'zone_name': zone_name,
                'title': title,
                'price': float(price.replace("'",'')),
                'marchant_credit': marchant_credit,
                'marchant_credit_icon': marchant_credit_icon,
                'publish_time': publish_time,
                'ensure': ensure,
                'goods_code': goods_code,
                'goods_title': goods_title,
                'goods_type': goods_type,
                'goods_price': float(goods_price.replace("'",'')),
                'goods_name': goods_game,
                'goods_os': goods_os,
                'etl_time':etl_time
            }

            filed_tuple = (
                'game_page_url','game_name','zone_name','title','price','marchant_credit','marchant_credit_icon','publish_time','ensure','goods_code','goods_title','goods_type','goods_price','goods_name','goods_os','etl_time')

            filed_values_tuple = tuple(item.values())
            self.insert_db(filed_tuple, filed_values_tuple)
            item_count += 1
            # print(threading.current_thread().name,' 插入第{}条数'.format(item_count),filed_values_tuple)

    def insert_db(self, filed_tuple, filed_values_tuple):
        try:
            sql = "insert into trade_5173_netgame_result({})values{}".format(','.join(filed_tuple), filed_values_tuple)
            self.cur.execute(sql)
            self.cur.execute('commit')
        except Exception as e:
            print(e)


GAME_QUEUE_NOT_EMPTY = True
HTML_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()
thread_write_lock = threading.Lock()


def main():
    # 游戏链接组成的队列
    game_url_queue = Queue()
    # 解析队列
    html_queue = Queue()

    with open("netgame_info.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    game_href_list = [line.split(",")[-1] for line in lines]
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