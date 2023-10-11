# _*_coding:utf-8 _*_

#@Time      : 2021/12/21  0:58
#@Author    : An
#@File      : main_multi_threading_7881.py
#@Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv,pymysql,threading
from queue import  Queue


class Trade7881Thread(threading.Thread):
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
            # print(self.game_url_queue.qsize())

            self.browser.get(game_url)
            self.check_next_page()
        self.browser.quit()

    def check_next_page(self):
        """
        :param browser:启动页面(点击某个游戏后首次跳转到的页面)
        :return:解析该页面后获取返回字段
        """
        # 显式等待
        wait = WebDriverWait(self.browser, 10)
        ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-sort')))

        # 单个游戏的首页里列表
        is_goods_exists = self.browser.page_source.find('抱歉，没有找到相关商品')
        if is_goods_exists != -1:
            # self.browser.close()
            return

        # 当前第N页
        laypage_cur = int(self.browser.find_element_by_class_name('laypage_curr').text)
        cur_page_url = self.browser.current_url
        cur_page_title = self.browser.title
        print(threading.current_thread().name,' ',cur_page_title,' ',cur_page_url,' 第 ',laypage_cur,'页列表')
        time.sleep(1)
        self.parse_next_page_detail(self.browser)

        laypage_main = self.browser.find_element_by_css_selector('.laypage_main.laypageskin_default')

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
        list_item_box = self.browser.find_elements_by_class_name('list-item-box')
        game_page_url = self.browser.current_url
        for item_box in list_item_box:
            txt_box = item_box.find_element_by_class_name('txt-box')
            try:
                title = txt_box.find_element_by_xpath("./h2/a/em[@class='tags icon-ptdf']").get_attribute(
                'title').strip().replace('\n', '')
            except:
                title = ''
            try:
                hot_num = txt_box.find_element_by_xpath("./h2/a/em[@class= 'hot-num']").text.strip().replace('\n', '')
            except:
                hot_num= ''
            try:
                desc = txt_box.find_element_by_xpath("./h2/a/span").text.strip().replace('\n', '')
            except:
                desc= ''
            try:
                zone_name = txt_box.find_element_by_xpath("./h4/span").text.strip().replace('\n', '')
            except:
                zone_name = ''
            try:
                goods_type = txt_box.find_elements_by_xpath("./p")[0].find_element_by_xpath("./span").text.strip().replace(
                '\n', '')
            except:
                goods_type = ''
            try:
                account_star = txt_box.find_elements_by_xpath("./p")[1].find_element_by_xpath("./span").get_attribute('class').replace('stars-box','').strip().replace('\n','')
            except:
                account_star = ''
            try:
                list_v = item_box.find_element_by_css_selector("[class= 'list-v part-02'").text.strip().replace('\n', '')
            except:
                list_v = ''

            tags_box = item_box.find_element_by_class_name('tags-box')
            try:
                shbz = tags_box.find_elements_by_xpath("./p")[0].text.strip().replace('\n', '')
            except:
                shbz= ''
            try:
                sfrz = tags_box.find_elements_by_xpath("./p")[1].text.strip().replace('\n', '')
            except:
                sfrz = ''

            try:
                list_btn = item_box.find_element_by_class_name('list-btn').text.strip().replace('\n', '')
            except:
                try:
                     list_btn = item_box.find_element_by_xpath("//span[@class = 'iconfont dealing']").get_attribute(
                        'class').strip().replace('\n', '')
                except:
                    try:
                        list_btn = item_box.find_element_by_css_selector(
                            "//span[@class='iconfont success']").get_attribute('class').strip().replace('\n', '')
                    except:
                        list_btn = ''

            zone_name_list = zone_name.split('/')
            game_name_ = zone_name_list[0]
            province_ = zone_name_list[1]
            zone_name_ = zone_name_list[2]

            item = {
                'game_page_url':game_page_url,
                'game_name':game_name_,
                'province':province_,
                'zone_name':zone_name_,
                'title': title,
                'hot_num': hot_num,
                'detail_desc': desc,
                'goods_type': goods_type,
                'account_star': account_star,
                'list_v': list_v,
                'shbz': shbz,
                'sfrz': sfrz
            }

            filed_tuple = (
            'game_page_url', 'game_name', 'province', 'zone_name', 'title', 'hot_num', 'detail_desc', 'goods_type',
            'account_star', 'list_v', 'shbz', 'sfrz')
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
            sql = "insert into trade_7881({})values{}".format(','.join(filed_tuple),filed_values_tuple)
            cur.execute(sql)
            cur.execute('commit')
        finally:
            cur.close()
            conn.close()

GAME_QUEUE_NOT_EMPTY = True
ITEM_QUEUE_NOT_EMPTY = True

def main():
    # 游戏链接组成的队列
    game_url_queue = Queue()
    # 解析队列
    item_parse_queue = Queue()

    start_url = 'https://account.7881.com/top'
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

    wait = WebDriverWait(browser, 10)
    ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gameList')))

    # 所有游戏url列表(游戏url可能有重复)
    game_href_list = []
    for game in browser.find_element_by_class_name('gameList').find_elements_by_xpath('//dd//a'):

        game_href_list.append(game.get_attribute('href'))
    for game in set(game_href_list):
        game_url_queue.put(game)

    trade_thread_name_list = ['trade' + str(i) for i in range(6)]
    trade_thread_list = []
    for thread_id in trade_thread_name_list:
        thread = Trade7881Thread(thread_id,game_url_queue)
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