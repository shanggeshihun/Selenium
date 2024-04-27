# _*_coding:utf-8 _*_

# @Time     :2023/11/18 15:54
# @Author   :anliu
# @File     :test_get_network_data.py
# @Theme    :Selenium获取Network数据（高级版）

DRIVER_PATH = r"E:\Program Files\chrome-win64\chromedriver.exe"

url = 'https://www.vvvdj.com/play/259632.html'


import json, time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

# 新版selenium模块将caps['loggingPrefs'] = {'performance': 'ALL'}修改为下方代码即可： 'goog:loggingPrefs': {'performance': 'ALL'}
caps = {
    "browserName": "chrome",
    'loggingPrefs': {'performance': 'ALL'}  # 开启日志性能监听
}
options = Options()
options.add_experimental_option('w3c', False)
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
browser = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=DRIVER_PATH)  # 启动浏览器
browser.get(url)  # 访问该url

time.sleep(3)

def filter_type(_type: str):
    types = [
        'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',
        'image/jpeg', 'image/x-icon', 'application/octet-stream'
    ]
    if _type not in types:
        return True
    return False


performance_log = browser.get_log('performance')  # 获取名称为 performance 的日志
for packet in performance_log:
    message = json.loads(packet.get('message')).get('message')  # 获取message的数据
    if message.get('method') != 'Network.responseReceived':  # 如果method 不是 responseReceived 类型就不往下执行
        continue
    packet_type = message.get('params').get('response').get('mimeType')  # 获取该请求返回的type
    if not filter_type(_type=packet_type):  # 过滤type
        continue
    requestId = message.get('params').get('requestId')  # 唯一的请求标识符。相当于该请求的身份证
    url = message.get('params').get('response').get('url')  # 获取 该请求  url
    try:
        resp = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})  # selenium调用 cdp
        print(f'type: {packet_type} url: {url}')
        print(f'response: {resp}')
        print()
    except WebDriverException:  # 忽略异常
        pass