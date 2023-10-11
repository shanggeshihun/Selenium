# _*_coding:utf-8 _*_

#@Time      : 2021/12/21  14:55
#@Author    : An
#@File      : parse_bak.py
#@Software  : PyCharm



#
# class ParseItemThread(threading.Thread):
#     def __init__(self,threading_id,game_url_queue,item_parse_queue):
#         threading.Thread.__init__(self)
#         self.game_url_queue = game_url_queue
#         self.item_parse_queue = item_parse_queue
#
#     def run(self):
#         while ITEM_QUEUE_NOT_EMPTY:
#             browser = self.item_parse_queue.get()
#
#             self.parse_next_page_detail(browser)
#
#     def parse_next_page_detail(self,browser):
#         """
#         :param browser: 单个游戏页面的browser
#         :return:
#         """
#         self.browser = browser
#         print(self.browser.current_url)
#         # print(self.browser.page_source)
#         list_item_box = self.browser.find_elements_by_class_name('list-item-box')
#         game_page_url = self.browser.current_url
#         for item_box in list_item_box:
#             txt_box = item_box.find_element_by_class_name('txt-box')
#             try:
#                 title = txt_box.find_element_by_xpath("./h2/a/em[@class='tags icon-ptdf']").get_attribute(
#                 'title').strip().replace('\n', '')
#             except:
#                 title = ''
#             print(title)
#             try:
#                 hot_num = txt_box.find_element_by_xpath("./h2/a/em[@class= 'hot-num']").text.strip().replace('\n', '')
#             except:
#                 hot_num= ''
#             print(hot_num)
#             try:
#                 desc = txt_box.find_element_by_xpath("./h2/a/span").text.strip().replace('\n', '')
#             except:
#                 desc= ''
#             try:
#                 zone_name = txt_box.find_element_by_xpath("./h4/span").text.strip().replace('\n', '')
#             except:
#                 zone_name = ''
#             try:
#                 goods_type = txt_box.find_elements_by_xpath("./p")[0].find_element_by_xpath("./span").text.strip().replace(
#                 '\n', '')
#             except:
#                 goods_type = ''
#             try:
#                 account_star = txt_box.find_elements_by_xpath("./p")[1].find_element_by_xpath("./span").get_attribute('class').replace('stars-box','').strip().replace('\n','')
#             except:
#                 account_star = ''
#             try:
#                 list_v = item_box.find_element_by_css_selector("[class= 'list-v part-02'").text.strip().replace('\n', '')
#             except:
#                 list_v = ''
#
#             try:
#                 tags_box = item_box.find_element_by_class_name('tags-box')
#             except:
#                 tags_box = ''
#             try:
#                 shbz = tags_box.find_elements_by_xpath("./p")[0].text.strip().replace('\n', '')
#             except:
#                 shbz= ''
#             try:
#                 sfrz = tags_box.find_elements_by_xpath("./p")[1].text.strip().replace('\n', '')
#             except:
#                 sfrz = ''
#
#             try:
#                 list_btn = item_box.find_element_by_class_name('list-btn').text.strip().replace('\n', '')
#             except:
#                 try:
#                      list_btn = item_box.find_element_by_xpath("//span[@class = 'iconfont dealing']").get_attribute(
#                         'class').strip().replace('\n', '')
#                 except:
#                     try:
#                         list_btn = item_box.find_element_by_css_selector(
#                             "//span[@class='iconfont success']").get_attribute('class').strip().replace('\n', '')
#                     except:
#                         list_btn = ''
#
#             zone_name_list = zone_name.split('/')
#             game_name_ = zone_name_list[0]
#             province_ = zone_name_list[1]
#             zone_name_ = zone_name_list[2]
#
#             item = {
#                 'game_page_url':game_page_url,
#                 'game_name':game_name_,
#                 'province':province_,
#                 'zone_name':zone_name_,
#                 'title': title,
#                 'hot_num': hot_num,
#                 'detail_desc': desc,
#                 'goods_type': goods_type,
#                 'account_star': account_star,
#                 'list_v': list_v,
#                 'shbz': shbz,
#                 'sfrz': sfrz
#             }
#
#             filed_tuple = (
#             'game_page_url', 'game_name', 'province', 'zone_name', 'title', 'hot_num', 'detail_desc', 'goods_type',
#             'account_star', 'list_v', 'shbz', 'sfrz')
#             filed_values_tuple = tuple(item.values())
#             self.insert_db(filed_tuple, filed_values_tuple)
#             print(item)
#
#     def insert_db(self,filed_tuple,filed_values_tuple):
#         try:
#             conn = pymysql.connect(
#                 host='localhost',
#                 user='root',
#                 passwd='052206',
#                 port=3306,
#                 db='test'
#             )
#             cur = conn.cursor()  # 数据库游标
#             cur.execute('SET NAMES utf8;')
#             cur.execute('SET CHARACTER SET utf8;')
#             cur.execute('SET character_set_connection=utf8;')
#         except Exception as e:
#             print(e)
#         else:
#             sql = "insert into trade_7881({})values{}".format(','.join(filed_tuple),filed_values_tuple)
#             print(sql)
#             cur.execute(sql)
#             cur.execute('commit')
#         finally:
#             cur.close()
#             conn.close()
