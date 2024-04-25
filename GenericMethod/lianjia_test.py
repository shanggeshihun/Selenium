# _*_coding:utf-8 _*_

#@Time      : 2021/12/20  12:04
#@Author    : An
#@File      : lianjia_test.py
#@Software  : PyCharm

# coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

'''
抓取链家网默认排序的房源信息
date：2019-11-17
Author:broccoli
'''

def write2txt(line):
    with open('./result.txt', 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def process():
    driver_path = r"D:\chromedriver.exe"
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.implicitly_wait(1)
    #实现页码拼接，第一页为一种情况，第2页以后要拼接上数字
    for page in range(1, 50):
        if page == 1:
            url = 'https://sh.lianjia.com/ershoufang/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=sousuo&ljref=pc_sem_baidu_ppzq_x'
        else:
            url = 'https://sh.lianjia.com/ershoufang/pg' + str(page) +'/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=sousuo&ljref=pc_sem_baidu_ppzq_x'

        browser.get(url)
        browser.maximize_window()
        wait = WebDriverWait(browser, 3)
        ul = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content  > div > ul')))
        li_list = ul.find_elements_by_tag_name('li')
        li_len = print(len(li_list))
        #添加num计数器是为了跳过第6个li元素，该元素下面没有文本内容，仅有一张广告图片
        num = 0
        for li in li_list:
            if num != 5:
                detail_div = li.find_element_by_css_selector('div')
                print(num)
                detail_div_list = detail_div.find_elements_by_tag_name('div')
                title = detail_div_list[0].find_element_by_tag_name('a').text
                print('房源：',title)
                write2txt('房源：'+title)
                flood_postition_list = detail_div_list[1].find_element_by_tag_name('div').find_elements_by_tag_name('a')
                print('房源位置：',flood_postition_list[0].text + flood_postition_list[1].text)
                write2txt('房源位置：' + flood_postition_list[0].text + flood_postition_list[1].text)
                #address = detail_div_list[2].find_element_by_css_selector('div.houseInfo').text
                #print(address)
                followInfo = detail_div_list[3].find_element_by_tag_name('div').text
                print('详细信息：', followInfo)
                write2txt('详细信息：'+ followInfo)
                #span_list = detail_div_list[4].find_elements_by_tag_name('span')
                #print(span_list[0].text + span_list[1].text)
            num += 1

if __name__ == '__main__':
    process()