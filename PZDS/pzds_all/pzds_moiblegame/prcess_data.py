# _*_coding:utf-8 _*_

#@Time      : 2021/12/30  17:36
#@Author    : An
#@File      : prcess_data.py
#@Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading
from queue import Queue
from lxml import etree

con = pymysql.connect(
    host='localhost',
    user='root',
    passwd='052206',
    port=3306,
    db='test'
)
cur = con.cursor()  # 数据库游标
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8')

select_sql = "select game_page_url, game_name, zone_name, title, price, server_protection, goods_code,goods_title, goods_type, goods_price, goods_name, goods_os from trade_5173_mobilegame_result_tmp"

cur.execute(select_sql)

select_result = cur.fetchall()

i = 0
for a  in  select_result:
    game_page_url=a[0].strip().replace("\n","")
    game_name=a[1].strip().replace("\n","")
    zone_name=a[2].strip().replace("\n","")
    title=a[3].strip().replace("\n","")
    price=a[4].strip().replace("\n","")
    server_protection=a[5].strip().replace("\n","")

    goods_code=a[6].strip().replace("\n","")[1:-1]
    goods_title=a[7].strip().replace("\n","")[1:-1]
    goods_type=a[8].strip().replace("\n","")[1:-1]
    goods_price=a[9].strip().replace("\n","")[1:-1]
    goods_name=a[10].strip().replace("\n","")[1:-1]
    goods_os=a[11].strip().replace("\n","")[1:-1]

    filed_values_tuple = (game_page_url,game_name,zone_name,title,price,server_protection,goods_code,goods_title,goods_type,goods_price,goods_name,goods_os)
    filed_tuple = (
        'game_page_url', 'game_name', 'zone_name', 'title', 'price', 'server_protection', 'goods_code',
        'goods_title', 'goods_type', 'goods_price', 'goods_name', 'goods_os')

    sql = "insert into trade_5173_mobilegame_result({})values{}".format(','.join(filed_tuple), filed_values_tuple)
    cur.execute(sql)
    i+=1
    print(i)
cur.execute('commit')
cur.close()
con.close()
#
#
# cur.fetchall()
#
#         goods_code = text_center[0][1:-1]
#         goods_title = text_center[1][1:-1]
#         goods_type = text_center[2][1:-1]
#         goods_price = text_center[3][1:-1]
#         goods_game = text_center[4][1:-1]
#         goods_os = text_center[5][1:-1]
#     except:
#         goods_code = ''
#         goods_title = ''
#         goods_type = ''
#         goods_price = ''
#         goods_game = ''
#         goods_os = ''
#
#     game_name = zone_name.split('-')[0]
#
#     item = {
#         'game_page_url': game_page_url,
#         'game_name': game_name,
#         'zone_name': zone_name,
#         'title': title,
#         'price': price,
#         'server_protection': server_protection,
#         'goods_code': goods_code,
#         'goods_title': goods_title,
#         'goods_type': goods_type,
#         'goods_price': goods_price,
#         'goods_name': goods_game,
#         'goods_os': goods_os
#     }
#
#     filed_tuple = (
#         'game_page_url', 'game_name', 'zone_name', 'title', 'price', 'server_protection', 'goods_code',
#         'goods_title', 'goods_type', 'goods_price', 'goods_name', 'goods_os')
#     filed_values_tuple = tuple(item.values())
#     self.insert_db(filed_tuple, filed_values_tuple)
#     item_count += 1
#     # print(threading.current_thread().name,' 插入第{}条数'.format(item_count),filed_values_tuple)
#
# try:
#     sql = "insert into trade_5173_mobilegame_result({})values{}".format(','.join(filed_tuple), filed_values_tuple)
#     self.cur.execute(sql)
#     self.cur.execute('commit')
# except Exception as e:
#     print(e)
