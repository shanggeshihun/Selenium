# _*_coding:utf-8 _*_

#@Time      : 2021/12/20  12:04
#@Author    : An
#@File      : test_anticrawl_by_direct.py
#@Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import time

driver_path = "E:\Program Files\chrome-win64\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=driver_path)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})


# browser.get('https://bot.sannysoft.com/')
browser.get('https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/28d?webSource=Total&key=bullgavial.com')
browser.quit()