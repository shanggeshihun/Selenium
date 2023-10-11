# _*_coding:utf-8 _*_

# @Time      : 2021/12/20  11:51
# @Author    : An
# @File      : main_single_threading_7881.py
# @Software  : PyCharm


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv,pymysql

class Trade7881(object):
    def __init__(self):
        self.start_url = 'https://account.7881.com/top'
        driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
        # 使用开发者模式
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(executable_path=driver_path)

    def run(self):
        self.game_url_list = self.game_list()
        for game in self.game_url_list:
            game_url = game.get_attribute('href')
            # if game_url in ['https://search.7881.com/list.html?pageNum=1&gameId=G10&gtid=100003','https://search.7881.com/list.html?pageNum=1&gameId=G5656&gtid=100003','','https://search.7881.com/list.html?pageNum=1&gameId=A5430&gtid=100003&mobileGameType=3']:
            #     continue
            print('当前爬取的游戏链接 {}'.format(game_url))
            game.click()
            self.check_next_page(self.browser)

    def game_list(self):
        """
        :start_url:所有游戏的页面url
        :return:
        """
        self.browser.get(self.start_url)
        self.browser.maximize_window()

        wait = WebDriverWait(self.browser, 3)
        ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gameList')))

        self.all_game_page_handle = self.browser.current_window_handle

        # 所有游戏url列表
        return self.browser.find_element_by_class_name('gameList').find_elements_by_tag_name("a")

    def check_next_page(self, browser):
        """
        :param browser:启动页面(点击某个游戏后首次跳转到的页面)
        :return:解析该页面后获取返回字段
        """

        # 单个游戏的首页里列表
        all_handles = self.browser.window_handles
        print('当前handles数量:',len(all_handles))

        for handle in all_handles:
            if handle != self.all_game_page_handle:
                cur_page_handle = handle
                browser.switch_to.window(cur_page_handle)

        is_goods_exists = self.browser.page_source.find('抱歉，没有找到相关商品')
        if is_goods_exists != -1:
            self.browser.close()
            self.browser.switch_to.window(self.all_game_page_handle)
            return

        wait = WebDriverWait(self.browser, 1)
        ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-sort')))

        # 当前第N页
        laypage_cur = int(self.browser.find_element_by_class_name('laypage_curr').text)
        print('当前游戏的第',laypage_cur,'页列表')
        self.parse_next_page_detail(self.browser)

        laypage_main = self.browser.find_element_by_css_selector('.laypage_main.laypageskin_default')

        # 查看 【下一页】是否存在
        page_num_tag_list = laypage_main.find_elements_by_tag_name('a')
        page_name_list = [page.text for page in page_num_tag_list]

        if '下一页' in page_name_list:
            next_page = laypage_main.find_element_by_link_text('下一页')
            next_page.click()
            self.check_next_page(browser)
        else:
            # 当该游戏的所有列表遍历完后切到起始页面
            self.browser.close()
            self.browser.switch_to.window(self.all_game_page_handle)
            return

        # # 关闭每个游戏的第N个页面
        # if laypage_cur > 1:
        #     self.browser.close()


    def parse_next_page_detail(self, browser):
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
            print(item)

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
            sql = 'insert into trade_7881({})values{}'.format(','.join(filed_tuple),filed_values_tuple)
            print(sql)
            cur.execute(sql)
            cur.execute('commit')
        finally:
            cur.close()
            conn.close()

if __name__ == '__main__':
    trade = Trade7881()
    trade.run()