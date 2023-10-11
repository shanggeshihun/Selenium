# _*_coding:utf-8 _*_
# @Time　　 : 2020/1/7   13:12
# @Author　 : zimo
# @File　   :1控制浏览器操作的一些方法.py
# @Software :PyCharm
# @Theme    :

from selenium import webdriver
import time
#1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
browser = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')
#2.通过浏览器向服务器发送URL请求
browser.get("https://www.baidu.com")
#3.刷新浏览器
browser.refresh()
#4.设置浏览器的大小
browser.set_window_size(1400,800)
#5.设置链接内容
element=browser.find_element_by_link_text("新闻")
element.click()
#5.设置链接内容
element=browser.find_element_by_link_text("音乐")
element.click()


input = driver.find_element_by_css_selector('#kw')
input.send_keys("风景照片")

button = driver.find_element_by_css_selector('#su')

button.click()
browser.quit()