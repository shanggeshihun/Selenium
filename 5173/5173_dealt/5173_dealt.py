# _*_coding:utf-8 _*_

# @Time      : 2022/5/12  11:52
# @Author    : An
# @File      : 5173_dealt.py
# @Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading,sys
from queue import Queue
from lxml import etree

start_url = 'http://trading.5173.com/list/ViewLastestDealList.aspx'
driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(executable_path=driver_path)
browser.maximize_window()
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
})

browser.get(start_url)

# wait = WebDriverWait(browser, 3)
# ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'game-list-ul clearfix')))

# netgame  netgame-hotspell
# mobilegame mobilegame-hotspell
# webgame webgame-hotspell

# 下拉游戏框
gs_name_arrow = browser.find_element_by_xpath("//li[@class='gs_name arrow']")
gs_name_arrow.click()

# 获取游戏以及序数
game_series_number = {}
for series_number,game_label in enumerate(browser.find_elements_by_xpath("//ul[@class='gs_list gs_name']/li")):
    game_series_number[game_label.text] = series_number
browser.quit()
print(game_series_number)
sys.exit()

gs_counts = len(game_series_number)

# 王者荣耀：86
for i in range(86,87):

    gs_name_arrow = browser.find_element_by_xpath("//li[@class='gs_name arrow']")
    gs_name_arrow.click()
    time.sleep(1)

    # 一级页面——某款游戏第N页的账号列表

    # 游戏标签
    game_labels = browser.find_elements_by_xpath("//ul[@class='gs_list gs_name']/li")

    the_game_label = game_labels[i]
    the_game_label.click()
    time.sleep(1)

    # 关闭筛选 按钮
    close_button = browser.find_element_by_xpath("//div[@class='gs_head clearfix']/a[@id='closeBtn']")
    close_button.click()
    time.sleep(1)

    # 查询按钮
    select_button = browser.find_element_by_xpath("//div[@id='_searchbox']/p[@class='clear']/a[@class='btn_g']")
    select_button.click()
    time.sleep(3)

    # 每页展示数量
    per_page_records_button = browser.find_element_by_xpath("//div[@class='paginal']/a[3]")
    per_page_records_button.click()
    time.sleep(3)

    list_main = browser.find_elements_by_xpath("//div[@class='listmain']/ul/li/a")

    for account in list_main:
        account.click()

        account_detail_html = browser.page_source
        html = etree.HTML(account_detail_html)

        main_area_info = html.xpath(r"//div[@class= 'dtliteminfo-wrap']")

        title = main_area_info.xpath(r"./div[@class = 'stfo-name']/text()")[0]
        price = main_area_info.xpath(r"./div[@class = 'stfo-summary']/div/div/em[2]/text()")[0]

        role_part = main_area_info.xpath(r"./div[@class = 'stfo-rolepart']")[0]
        role_part_district = role_part.xpath(r"./ul[@class='district']/li/span[2]/text()")[0]

        time.sleep(10)
        browser.quit()
        break
    break

browser.quit()

time.sleep(2)

#     # 游戏基本信息保存到文件
#     f = open("./mobilegame_info.txt","w",encoding="utf-8")
#
#     first_letter = browser.find_elements_by_xpath("//ul[@class='tab-letter clearfix']/li")
#
#     for fl in first_letter:
#         tmp_game_href_list = []
#         if fl.get_attribute('class') == 'hot':
#             continue
#         fl.click()
#         time.sleep(4)
#
#         game_first_letter=fl.text
#
#         # 单独测试某字母开头游戏的加载情况
#         # if game_first_letter !='W':
#         #     continue
#         browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         time.sleep(5)
#         game_xpath_name = "//ul[@class='gamelist-ul clearfix mobilegame-{}']/li/a[@class='link-all']".format(game_first_letter)
#
#         g = browser.find_elements_by_xpath(game_xpath_name)
#
#         game_count = 0
#         if not g:
#             continue
#         else:
#
#             for game in g:
#                 game_href = game.get_attribute('href')
#                 game_name = game.find_element_by_xpath("./p[@class='name']").text
#                 game_count+=1
#
#                 f.writelines((game_first_letter,",",game_name,",",game_href,"\n"))
#             print("{}-字母开头的游戏有-{}-款".format(game_first_letter,game_count))
#     browser.close()
#     browser.quit()
#     f.close()
#
# def test_wrirelines():
#     f = open("./netgame_info_bak.txt", "w", encoding="utf-8")
#     for a in [1, 2, 3]:
#         f.writelines((str(a), str(a), str(a), "\n"))
#
#     for a in [11, 22, 33]:
#         f.writelines((str(a), str(a), str(a), "\n"))
#     f.close()
#     f.close()
#
# def test_wrirelines_2():
#     f = open("./netgame_info_bak.txt", "w", encoding="utf-8")
#     for a in [4, 5, 6]:
#         f.writelines((str(a), str(a), str(a), "\n"))
#     f.close()
#
# def test_read():
#     f = open("./netgame_info_bak.txt", "r", encoding="utf-8")
#     lines = f.readlines()
#     print("打印行数",len(lines))
#     for line in lines:
#         print('当前打印',line)
#     f.close()
#
# if __name__ == '__main__':
#     # test_wrirelines()
#     # test_wrirelines_2()
#     mobilegame_info()
