# _*_coding:utf-8 _*_

#@Time      : 2021/12/20  0:44
#@Author    : An
#@File      : main_single_threading_7881.py
#@Software  : PyCharm

'''
多进程抓取深圳证券交易所本所公告数据
标题和公告内容写入了不同的csv文件里
'''

from selenium import webdriver
import time
import csv
from multiprocessing import Process

def process(start,end,num):
    driver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    #使用开发者模式
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

    browser.implicitly_wait(1)

    # j 第j页公告列表
    for j in range(start,end):
        if(j==1):
            url="http://www.szse.cn/disclosure/notice/index.html"
        else:
            url="http://www.szse.cn/disclosure/notice/index_"+str(j-1)+".html"
        print('开始爬取第{}页 {}'.format(j,url))
      # if(j%10==0):#每处理10页数据，关闭并重启一次浏览器
      #     browser.quit()
      #     browser = webdriver.Chrome(executable_path=driver_path)

        # 每页20条公告
        for i in range(20):
            browser.get(url)
            browser.maximize_window()
            print("####################################################第",j,"页，第",i,"条记录")
            # 获取列表页handle
            list_page_handle = browser.current_window_handle
            div_content = browser.find_element_by_class_name('g-content-list')
            li_list = div_content.find_elements_by_tag_name('li')
            a_href = li_list[i].find_element_by_tag_name('a').get_attribute('href')
            if(a_href.find('.pdf')>0 or a_href.find('.doc')>0 or a_href.find('.DOC')>0):
                continue
            print(a_href)
            # 点击进入公告详情页
            li_list[i].find_element_by_tag_name('a').click()
            # 当前出现2个窗口：公告列表以及某条详情
            all_handles = browser.window_handles
            # 进入详情页
            for handle in all_handles:
                if (handle != list_page_handle):
                    browser.switch_to.window(handle)
            #标题
            title_div = browser.find_element_by_class_name('des-header')
            title_h2 = title_div.find_element_by_tag_name('h2')
            print(title_h2.text)
            data_row_title = [title_h2.text]
            with open('./data/sz_data_title' + str(num) + '.csv', 'a+', newline="", encoding='utf-8') as f:
            with open('./data/sz_data_title' + str(num) + '.csv', 'a+', newline="", encoding='utf-8') as f:
                csv_add = csv.writer(f)
                csv_add.writerow(data_row_title)
            #公告内容
            content_div = browser.find_element_by_id('desContent')
            p_content_list = content_div.find_elements_by_tag_name('p')
            final_text=""
            for p in p_content_list:
                final_text+=p.text.strip()
            print(final_text)
            data_row = [final_text]
            with open('./data/sz_data'+ str(num) +'.csv', 'a+', newline="",encoding='utf-8') as f:
                csv_add = csv.writer(f)
                csv_add.writerow(data_row)
            time.sleep(1)

            # 关闭详情页
            browser.close()
            # 切换到列表页
            browser.switch_to.window(list_page_handle)

def main():
    #开启4个进程，传入爬取的页码范围
    process_list = []
    p1 = Process(target=process, args=(1,3,1))
    p1.start()
    p2 = Process(target=process, args=(4, 7,1))
    p2.start()
    # p3 = Process(target=process, args=(800, 1000, 1))
    # p3.start()
    # p4 = Process(target=process, args=(1000, 1129, 1))
    # p4.start()
    process_list.append(p1)
    process_list.append(p2)
    # process_list.append(p3)
    # process_list.append(p4)
    for t in process_list:
        t.join()

if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print('总用时：',e-s)