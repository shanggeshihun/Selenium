# _*_coding:utf-8 _*_

# @Time      : 2021/12/20  11:51
# @Author    : An
# @File      : main_single_threading_7881.py
# @Software  : PyCharm


from selenium import webdriver
import time, csv

driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# 使用开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 所有游戏列表页面
browser = webdriver.Chrome(executable_path=driver_path)
url = 'https://account.7881.com/top'
browser.get(url)
browser.maximize_window()
all_game_page_handle = browser.current_window_handle

# 所有游戏url列表
game_url_list = browser.find_elements_by_xpath("//div[@class='gameList']/dl")

for game in game_url_list:
    game_url = game.find_element_by_tag_name('a').get_attribute('href')
    print('当前爬取的游戏链接 {}'.format(game_url))
    game.click()

    # 单个游戏的首页里列表
    all_handles = browser.window_handles
    for handle in all_handles:
        if handle != all_game_page_handle:
            browser.switch_to.window(handle)
    game_zone=browser.find_elements_by_xpath("//div[@class='txt-box']/h4/span")
    for z in game_zone:
        print(z.text)
    # browser.close()
    time.sleep(5)

    # 查看 【下一页】是否存在
    laypage_main = browser.find_element_by_css_selector('.laypage_main.laypageskin_default')
    page_num_tag_list = laypage_main.find_elements_by_tag_name('a')
    page_name_list = [page.text for page in page_num_tag_list]
    if '下一页' in page_name_list:
        next_page = laypage_main.find_element_by_link_text('下一页')
        next_page.click()



    browser.switch_to.window(all_game_page_handle)


def parse_detail(browser):
    """
    :param browser:启动页面(点击某个游戏后首次跳转到的页面)
    :return:解析该页面后获取返回字段
    """
    # 单个游戏的首页里列表
    all_handles = browser.window_handles
    for handle in all_handles:
        if handle != all_game_page_handle:
            browser.switch_to.window(handle)
    game_zone = browser.find_elements_by_xpath("//div[@class='txt-box']/h4/span")
    for z in game_zone:
        print(z.text)
    # browser.close()
    time.sleep(5)

    # 查看 【下一页】是否存在
    laypage_main = browser.find_element_by_css_selector('.laypage_main.laypageskin_default')
    page_num_tag_list = laypage_main.find_elements_by_tag_name('a')
    page_name_list = [page.text for page in page_num_tag_list]
    if '下一页' in page_name_list:
        next_page = laypage_main.find_element_by_link_text('下一页')
        next_page.click()
        parse_detail(browser)
    return