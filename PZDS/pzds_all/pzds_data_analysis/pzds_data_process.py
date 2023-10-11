# _*_coding:utf-8 _*_

# @Time      : 2022/5/11  14:30
# @Author    : An
# @File      : pzds_data_process.py
# @Software  : PyCharm
from OperateMysql import OperateMysql

# MySQL连接配置
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = '052206'
mysql_database = 'test'
mysql_port = 3306

# 实例化mysql
operate_mysql = OperateMysql(
    username=mysql_user,
    password=mysql_password,
    host_ip=mysql_host,
    port=int(mysql_port),
    database=mysql_database
)

# mysql sql操作语句
mysql_sql = """
   select distinct game_page_url, game_id, game_name, goods_code, goods_title,goods_serve,goods_price, goods_deal_status 
from pzds 
where game_name in ('王者荣耀')
"""
try:
    result_data = operate_mysql.query_data(mysql_sql)
    result_data_columns = operate_mysql.query_data_index()
except Exception as e:
    operate_mysql.close_conn()
    print(e)
else:
    # print(result_data)
    # print(result_data_columns)
    operate_mysql.close_conn()

import re

goods_info_list = []
for tup in result_data:
    game_name = tup[2]
    goods_code = tup[3]
    goods_title = tup[4]

    goods_serve = tup[5]
    serve_pattern = re.compile(r"(\d+-\d+)")
    goods_serve_ = serve_pattern.findall(goods_serve)[0]

    goods_price =tup[6]

    goods_title_pattern = re.compile(r"【(.*?)(QQ|微信).*】.*【(.*?)】\s*贵族(\d+)\s*荣耀水晶(\d+)\s*英雄(\d+)\s*皮肤(\d+)\s*(.*?)\s*营地.*?(\d+)")

    goods_title_info_list = goods_title_pattern.findall(goods_title)

    os = goods_title_info_list[0][0]
    source = goods_title_info_list[0][1]
    user_auth_type = goods_title_info_list[0][2]
    vip_grade = goods_title_info_list[0][3]
    honor_crystal = goods_title_info_list[0][4]
    heros = goods_title_info_list[0][5]
    skin_numbers = goods_title_info_list[0][6]
    dw = goods_title_info_list[0][7]
    winner_club_account = goods_title_info_list[0][8]

    goods_info_tup_tmp = (game_name,goods_code,goods_serve_,goods_price,os,source,user_auth_type,vip_grade,honor_crystal,heros,skin_numbers,dw,winner_club_account)

    goods_info_list.append(goods_info_tup_tmp)

import pandas as pd
df = pd.DataFrame(goods_info_list)
df.columns = ['game_name','goods_code','goods_serve_','goods_price','os','source','user_auth_type','vip_grade','honor_crystal','heros','skin_numbers','dw','winner_club_account']
df.to_csv(r"./pzds_data_process.csv")





