# _*_coding:utf-8 _*_

#@Time      : 2021/12/16  22:39
#@Author    : An
#@File      : get_webgame_info.py
#@Software  : PyCharm


#

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.suicideboysmerchandise.com/'
url = 'https://rockgrouphoodie.com/payments/landing/return/bdc6eb3c-5bbc-4f8a-a4ec-4bca23dd2061?spm=onerway.hosted&origin_host=aHR0cHM6Ly93d3cuc3VpY2lkZWJveXNtZXJjaGFuZGlzZS5jb20=&t_id=2bb6aa1e-1834-4acf-8bca-af9f92666130'

chrome_options = Options()
chrome_options.add_argument('--headless')  # 启用无头模式

driver = webdriver.Chrome(r'E:\Program Files\chrome-win64\chromedriver.exe')
driver.get(url)

# 等待页面加载完成，最多等待10秒钟
time.sleep(2)

print('11')
print(driver.current_url)
driver.quit()