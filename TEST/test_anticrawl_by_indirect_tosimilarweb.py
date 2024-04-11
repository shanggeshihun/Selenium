# _*_coding:utf-8 _*_

#@Time      : 2021/12/20  12:04
#@Author    : An
#@File      : test_anticrawl_by_indirect.py
#@Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import time

browser_path = "E:\Program Files\chrome-win64\chrome.exe"

subprocess.Popen([browser_path, '--remote-debugging-port=9222'])

time.sleep(3)

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(executable_path="E:\Program Files\chrome-win64\chromedriver.exe", options=options)

driver.get('https://pro.similarweb.com/#/digitalsuite/home')
driver.quit()