# _*_coding:utf-8 _*_

#@Time      : 2021/12/22  11:35
#@Author    : An
#@File      : main_multi_threading_dd373_parseclass.py
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

# 预警邮件提醒
from WarningEmail import warning_email


import sys
sys.setrecursionlimit(20000)

class TradeDd373Thread(threading.Thread):
    def __init__(self,thread_id,game_url_queue,html_queue):
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
        self.html_queue = html_queue

    def run(self):
        """
        :start_url:游戏的初始url
        :return:初始化browser对象
        """
        while GAME_QUEUE_NOT_EMPTY:
            start_url = self.game_url_queue.get()
            self.game_url_queue.task_done()
            print('GAME_QUEUE_NOT_EMPTY:',1)

            self.game_account_page(start_url)

            self.check_next_page()
        self.browser.quit()

    def game_account_page(self,start_url):
        """
        :param start_url: 某游戏起始页面
        :return: 某游戏的交易账号页面
        """
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
        wait = WebDriverWait(self.browser, 20)
        ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-pagination-container')))

        # 当前第N页
        while True:
            try:
                laypage_cur = int(self.browser.find_element_by_css_selector("[class = 'ui-pagination-page-item active']").text)
            except Exception as e:
                print('【异常】手工处理:',e)
                time.sleep(180)
                self.browser.refresh()
            else:
                break

        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title
        print(threading.current_thread().name,' ',cur_page_title,' ',cur_page_url,' 第 ',laypage_cur,'页列表')
        time.sleep(1)

        # 每个处理20页，等待30秒
        if laypage_cur % 20 == 0:
            time.sleep(30)

        # 每个处理70页，等待60秒
        if laypage_cur % 70 == 0:
            time.sleep(60)

        # 页面链接+页面page_source均写入队列
        self.html_queue.put((cur_page_url,self.browser.page_source))
        print('页面链接+页面page_source均写入队列',self.html_queue.qsize)

        laypage_main = self.browser.find_element_by_class_name('ui-pagination-container')

        # 查看 【下一页】是否存在
        page_num_tag_list = laypage_main.find_elements_by_tag_name('a')
        page_name_list = [page.text for page in page_num_tag_list]

        if '下一页' in page_name_list:
            next_page = laypage_main.find_element_by_link_text('下一页')
            next_page.click()

            """
            点击下一页等待2秒，作3次尝试。
            第一次：如果等待后下一页页码比上一页大1，则加载完成，跳出尝试，否则再等待5秒
            第二次：如果第一次等待5秒后，仍没有加载到下一页，则刷新页面，并等待5秒
            第三次：仍没有加载完，则数据重复
            """
            time.sleep(2)
            # 确定有下一页时，点击后检查是否正常跳转到了新页面
            check_times = 0
            while check_times< 3 :
                # 当前第N页
                next_page_num = int(
                    self.browser.find_element_by_css_selector("[class = 'ui-pagination-page-item active']").text)
                if next_page_num == laypage_cur + 1:
                    print('           【成功】加载下一页，尝试第{}次后'.format(check_times))
                    break
                else:
                    if check_times == 1:
                        self.browser.refresh()
                        print('           【刷新】页面，尝试第{}次后'.format(check_times))
                    time.sleep(5)
                    check_times +=1
            if check_times == 3:
                print('           【未知】加载下一页，尝试第{}次后加，等待下次尝试'.format(check_times))
            self.check_next_page()
        else:
            # 从起始页到最后一次页遍历完成
            self.browser.close()
            return

class ParseTradeDd373Thread(threading.Thread):
    def __init__(self,thread_id,html_queue):
        """
        :param thread_id: 爬虫线程
        :param html_queue: 页面链接 + 页面page_source 为元组元素的队列
        """
        threading.Thread.__init__(self)
        self.html_queue = html_queue
        self.con =pymysql.connect(
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
        time.sleep(10)
        print('启动前self.html_queue.empty()',self.html_queue.empty())
        while HTML_QUEUE_NOT_EMPTY:
            try:
                print('启动时self.html_queue.empty()', self.html_queue.empty())
                html =self.html_queue.get(False)
                print('html\n',html)
                self.html_queue.task_done()
                self.parse_next_page_detail(html)
            except:
                pass
        self.cur.close()
        self.con.close()
        print('启动结束后self.html_queue.qsize()', self.html_queue.qsize())
        print('关闭数据库连接')


    def parse_next_page_detail(self,html):
        """
        :param browser: 单个游戏页面的browser
        :return:
        """
        game_page_url = html[0]
        page_source = html[1]
        html = etree.HTML(page_source)
        goods_list_item = html.xpath("//div[@class = 'goods-list-item']")

        item_count = 1
        for item_box in goods_list_item:

            try:
                title = item_box.xpath(".//div[@class = 'game-account-flag']/text()")
                title = ''.join([t.strip().replace("\n", "") for t in title])
            except:
                title = ''

            try:
                zone_name = html.xpath(
            ".//p[contains(@class,'game-qufu-attr normalGoodsArea')]/span[2]/a")
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
                'trust_grade':trust_grade,
                'goods_price':goods_price,
                'kucun':kucun,
                'server_protection':server_protection
            }

            filed_tuple = (
            'game_page_url', 'game_name', 'zone_name', 'title', 'trust_grade', 'goods_price', 'kucun', 'server_protection')
            filed_values_tuple = tuple(item.values())
            self.insert_db(filed_tuple, filed_values_tuple)
            item_count +=1
            print('插入了第{}条数据'.format(item_count),filed_values_tuple)

    def insert_db(self,filed_tuple,filed_values_tuple):
        try:
            sql = "insert into trade_dd373_test({})values{}".format(','.join(filed_tuple),filed_values_tuple)
            self.cur.execute(sql)
            self.cur.execute('commit')
        except Exception as e:
            print(e)


GAME_QUEUE_NOT_EMPTY = True
HTML_QUEUE_NOT_EMPTY = True

thread_lock = threading.Lock()

def main():
    # 游戏链接组成的队列
    game_url_queue = Queue()
    # 解析队列
    html_queue = Queue()

    start_url = 'https://game.dd373.com/y-0-1.html'
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
    while repeat_times <=3:
        try:
            browser.get(start_url)
        except:
            repeat_times += 1
        else:
            break

    # wait = WebDriverWait(browser, 3)
    # ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'game-list-ul clearfix')))

    # 所有游戏url列表(游戏url可能有重复)
    game_href_list = []
    for game in browser.find_elements_by_xpath("//ul[@class = 'game-list-ul clearfix']/li/a"):
        game_href_list.append(game.get_attribute('href'))
    browser.quit()
    for game in set(game_href_list):
        if game in ['https://www.dd373.com/s-g2gdhs.html']:
         game_url_queue.put(game)

    trade_thread_name_list = ['trade' + str(i) for i in range(1)]
    trade_thread_list = []
    for thread_id in trade_thread_name_list:
        thread = TradeDd373Thread(thread_id,game_url_queue,html_queue)
        thread.start()
        trade_thread_list.append(thread)

    parse_thread_name_list = ['parse' + str(i) for i in range(1)]
    parse_thread_list = []
    for thread_id in parse_thread_name_list:
        thread = ParseTradeDd373Thread(thread_id,html_queue)
        thread.start()
        parse_thread_list.append(thread)

    while not game_url_queue.empty():
        pass
    global GAME_QUEUE_NOT_EMPTY
    GAME_QUEUE_NOT_EMPTY = False
    print("GAME_QUEUE为空")

    for t in trade_thread_list:
        t.join()
    print('爬虫程序已结束')


    while not html_queue.empty():
        pass
    global HTML_QUEUE_NOT_EMPTY
    HTML_QUEUE_NOT_EMPTY = False
    print("HTML_QUEUE为空")
    print('Program a is running... at ', '.线程名为：', threading.current_thread().name)
    for t in parse_thread_list:
        t.join()
    print('解析程序已经结束')
    #print('Program a is running... at ', '.线程名为：', threading.current_thread().name)

if __name__ == '__main__':
    start_time = time.time()
    print('start_time:',start_time)
    main()
    print(time.time()-start_time)