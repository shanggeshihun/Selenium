# _*_coding:utf-8 _*_
# @Time　　 : 2020/1/13   1:38
# @Author　 : zimo
# @File　   :2鼠标事件.py
# @Software :PyCharm
# @Theme    :


# 在 WebDriver 中， 将这些关于鼠标操作的方法封装在 ActionChains 类提供。

from selenium import webdriver
#1.引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
browser= webdriver.Chrome()
browser.get("https://www.baidu.cn")
#2.定位到要悬停的元素
element= browser.find_element_by_link_text("设置")
#3.对定位到的元素执行鼠标悬停操作
ActionChains(browser).move_to_element(element).perform()