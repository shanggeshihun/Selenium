# _*_coding:utf-8 _*_
# @Time　　 : 2020/1/14   1:04
# @Author　 : zimo
# @File　   :4获取断言信息.py
# @Software :PyCharm
# @Theme    :
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()
browser.get("https://www.baidu.com")

print('Before search================')

# 打印当前页面title
title = browser.title
print(title)

# 打印当前页面URL
now_url = browser.current_url
print(now_url)

browser.find_element_by_id("kw").send_keys("selenium")
browser.find_element_by_id("su").click()
sleep(1)

print('After search================')

# 再次打印当前页面title
title = browser.title
print(title)

# 打印当前页面URL
now_url = browser.current_url
print(now_url)

# 获取结果数目
user = browser.find_element_by_class_name('nums').text
print(user)

#关闭所有窗口
browser.quit()