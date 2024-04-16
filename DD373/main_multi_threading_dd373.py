# _*_coding:utf-8 _*_

#@Time      : 2021/12/21  14:03
#@Author    : An
#@File      : main_multi_threading_dd373.py
#@Software  : PyCharm

"""
一级页面 ：所有游戏
二级页面 ：点击单个游戏进入的页面，该页面需要通过选择【商品类型】获取账号交易的网站地址
三级页面 ：单个游戏账号交易的网站地址
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv,pymysql,threading
from queue import  Queue
from lxml import etree

class TradeDd373Thread(threading.Thread):
    def __init__(self,thread_id,game_url_queue):
        threading.Thread.__init__(self)
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

    def run(self):
        """
        :start_url:游戏的初始url
        :return:初始化browser对象
        """
        while GAME_QUEUE_NOT_EMPTY:
            game_url = self.game_url_queue.get()
            print(self.game_url_queue.qsize())

            self.game_account_page(game_url)
            self.check_next_page()
        self.browser.quit()

    def game_account_page(self,star_url):
        """
        :param star_url: 某游戏起始页面
        :return: 某游戏的交易账号页面
        """
        start_url = self.game_url_queue.get()
        self.game_url_queue.task_done()
        self.browser.get(start_url)
        goods_select_value=self.browser.find_element_by_class_name("goods-select-value")
        goods_select = goods_select_value.find_elements_by_tag_name("a")
        choice_list = []
        for choice in goods_select:
            choice_list.append(choice.text)
        if  '游戏帐号' in choice_list:
            return goods_select_value.find_element_by_link_text("游戏帐号").click()


    def check_next_page(self):
        """
        :param browser:启动页面(点击某个游戏后首次跳转到的页面)
        :return:解析该页面后获取返回字段
        """
        # 显式等待
        wait = WebDriverWait(self.browser, 10)
        ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'good-list-box')))

        # # 单个游戏的首页里列表
        # is_goods_exists = self.browser.page_source.find('抱歉，没有找到相关商品')
        # if is_goods_exists != -1:
        #     # self.browser.close()
        #     return

        # 当前第N页
        laypage_cur = int(self.browser.find_element_by_css_selector("[class = 'ui-pagination-page-item active']").text)
        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title
        print(threading.current_thread().name,' ',cur_page_title,' ',cur_page_url,' 第 ',laypage_cur,'页列表')
        time.sleep(1)
        self.parse_next_page_detail(self.browser)

        laypage_main = self.browser.find_element_by_class_name('ui-pagination-container')

        # 查看 【下一页】是否存在
        page_num_tag_list = laypage_main.find_elements_by_tag_name('a')
        page_name_list = [page.text for page in page_num_tag_list]

        if '下一页' in page_name_list:
            next_page = laypage_main.find_element_by_link_text('下一页')

            try_times = 0
            while try_times <= 3:
                try:
                    next_page.click()
                except:
                    try_times += 1
                else:
                    break
            self.check_next_page()
        else:
            # 当该游戏的所有列表遍历完后切到起始页面
            # self.browser.close()
            return

    def parse_next_page_detail(self,browser):
        """
        :param browser: 单个游戏页面的browser
        :return:
        """
        goods_list_item = self.browser.find_elements_by_class_name('goods-list-item')
        game_page_url = self.browser.current_url
        page_source = self.browser.page_source

        html = etree.HTML(page_source)

        goods_list_item = html.xpath("//div[@class = 'goods-list-item']")

        for item_box in goods_list_item:

            try:
                title = item_box.xpath(".//div[@class = 'game-account-flag']/text()")
                title = ''.join([t.strip().replace("\n", "") for t in title])
            except:
                title = ''

            try:
                zone_name = html.xpath(
            ".//p[@class='game-qufu-attr normalGoodsArea0']/span[2]/a")
                zone_name = '/'.join([z.xpath("./text()")[0] for z in zone_name])
            except:
                zone_name = ''

            try:
                trust_grade = len(item_box.xpath(".//p[@class='game-reputation']/i"))
            except:
                trust_grade = ''

            try:
                goods_price= item_box.xpath("./div[@class= 'goods-price ']/span/text()")[0]

            except:
                goods_price = ''

            try:
                kucun = item_box.xpath("./div[@class= 'kucun ']/span/text()")[0]
            except:
                kucun = ''

            try:
                server_protection =item_box.xpath("./div[@class= 'server-protection ']/a/span")
                server_protection= '/'.join(s.xpath("./text()")[0] for s in server_protection)
            except:
                server_protection = ''

            game_name = zone_name.split('/')[0]

            item = {
                'game_page_url':game_page_url,
                'game_name':game_name,
                # 'province':province_,
                'zone_name':zone_name,
                'title': title,
                # 'hot_num': hot_num,
                # 'detail_desc': desc,
                # 'goods_type': goods_type,
                # 'account_star': account_star,
                # 'list_v': list_v,
                # 'shbz': shbz,
                # 'sfrz': sfrz
                'trust_grade':trust_grade,
                'goods_price':goods_price,
                'kucun':kucun,
                'server_protection':server_protection
            }

            filed_tuple = (
            'game_page_url', 'game_name', 'zone_name', 'title', 'trust_grade', 'goods_price', 'kucun', 'server_protection')
            filed_values_tuple = tuple(item.values())
            self.insert_db(filed_tuple, filed_values_tuple)

    def insert_db(self,filed_tuple,filed_values_tuple):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                passwd='052206',
                port=3306,
                db='test'
            )
            cur = conn.cursor()  # 数据库游标
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
        except Exception as e:
            print(e)
        else:
            sql = "insert into trade_dd373({})values{}".format(','.join(filed_tuple),filed_values_tuple)
            cur.execute(sql)
            cur.execute('commit')
        finally:
            cur.close()
            conn.close()

GAME_QUEUE_NOT_EMPTY = True
ITEM_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()

def main():
    # 游戏链接组成的队列
    game_url_queue = Queue()
    # 解析队列
    item_parse_queue = Queue()

    start_url = 'https://game.dd373.com/y-0-1.html'
    driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    # 使用开发者模式
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path=driver_path)


    repeat_times = 0
    while repeat_times <=3:
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
        game_href_list.append(game.get_attribute('href'))
    for game in set(game_href_list):
        game_url_queue.put(game)

    trade_thread_name_list = ['trade' + str(i) for i in range(5)]
    trade_thread_list = []
    for thread_id in trade_thread_name_list:
        thread = TradeDd373Thread(thread_id,game_url_queue)
        thread.start()
        trade_thread_list.append(thread)

    while not game_url_queue.empty():
        pass
    global GAME_QUEUE_NOT_EMPTY
    GAME_QUEUE_NOT_EMPTY = False

    for t in trade_thread_list:
        t.join()


if __name__ == '__main__':
    main()