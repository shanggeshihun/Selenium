# _*_coding:utf-8 _*_

#@Time      : 2021/12/25  22:28
#@Author    : An
#@File      : 页面信息.py
#@Software  : PyCharm


"""
一、从 http://www.5173.com/ 进入爬虫游戏不全面
见 main_multi_threading_5173_webgame_all.py
主页面游戏分为三大块：
a）网络游戏："全部商品"》"游戏帐号"
b）手机游戏:"选择商品"》"账号"
c）网页游戏:"全部商品"》"游戏账号"

一级页面 ：所有游戏
二级页面 ：点击单个游戏进入的页面，该页面需要通过选择【商品类型】获取账号交易的网站地址
三级页面 ：单个游戏账号交易的网站地址

二、从http://sy.5173.com/ 进入爬虫
见
一级页面：http://sy.5173.com/
a)点击【游戏名称】下拉框》点击【网络游戏】》点击游戏某款游戏》点击【搜索】
进入二级页面
二级页面：某款游戏的页面
"""


