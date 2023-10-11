# _*_coding:utf-8 _*_

# @Time      : 2021/12/29  17::25
# @Author    : An
# @File      : get_webgame_info.py
# @Software  : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, csv, pymysql, threading
from queue import Queue
from lxml import etree

def netgame_info():
    start_url = 'http://www.5173.com/'
    driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    # 使用开发者模式
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

    repeat_times = 0
    while repeat_times <= 3:
        try:
            browser.get(start_url)
        except:
            repeat_times += 1
        else:
            break

    # wait = WebDriverWait(browser, 3)
    # ul = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'game-list-ul clearfix')))

    # mobilegame  mobilegame-hotspell
    # netgame netgame-hotspell
    # webgame webgame-hotspell
    netgame_bnt = browser.find_element_by_xpath("//li[@data-tab='netgame']")
    netgame_bnt.click()
    time.sleep(2)


    # 游戏基本信息保存到文件
    f = open("./netgame_info_bak.txt","w",encoding="utf-8")

    first_letter = browser.find_elements_by_xpath("//ul[@class='tab-letter clearfix']/li")

    for fl in first_letter:
        tmp_game_href_list = []
        if fl.get_attribute('class') == 'hot':
            continue
        fl.click()
        time.sleep(2)

        game_first_letter=fl.text

        game_xpath_name = "//ul[@class='gamelist-ul clearfix netgame-{}']/li/a[@class='link-all']".format(game_first_letter)

        g = browser.find_elements_by_xpath(game_xpath_name)

        game_count = 0
        if not g:
            continue
        else:

            for game in g:
                game_href = game.get_attribute('href')
                game_name = game.find_element_by_xpath("./p[@class='name']").text
                game_count+=1

                f.writelines((game_first_letter,",",game_name,",",game_href,"\n"))
            print("{}-字母开头的游戏有-{}-款".format(game_first_letter,game_count))
    browser.close()
    browser.quit()
    f.close()

def test_wrirelines():
    f = open("./netgame_info_bak.txt", "w", encoding="utf-8")
    for a in [1, 2, 3]:
        f.writelines((str(a), str(a), str(a), "\n"))

    for a in [11, 22, 33]:
        f.writelines((str(a), str(a), str(a), "\n"))
    f.close()
    f.close()

def test_wrirelines_2():
    f = open("./netgame_info_bak.txt", "w", encoding="utf-8")
    for a in [4, 5, 6]:
        f.writelines((str(a), str(a), str(a), "\n"))
    f.close()

def test_read():
    f = open("./netgame_info_bak.txt", "r", encoding="utf-8")
    lines = f.readlines()
    print("打印行数",len(lines))
    for line in lines:
        print('当前打印',line)
    f.close()

if __name__ == '__main__':
    # test_wrirelines()
    # test_wrirelines_2()
    netgame_info()