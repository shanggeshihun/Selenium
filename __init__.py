# _*_coding:utf-8 _*_

#@Time      : 2021/12/26  21:50
#@Author    : An
#@File      : __init__.py.py
#@Software  : PyCharm

import threading
import requests
from bs4 import BeautifulSoup
import mysql.connector
from queue import Queue

# 定义数据库连接参数
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_database_name',
}

# 创建队列来存储爬取的数据
data_queue = Queue()

# 生产者类，用于爬取数据并将其放入队列
class Producer(threading.Thread):
    def __init__(self, urls):
        super(Producer, self).__init__()
        self.urls = urls

    def crawl_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').get_text()
                content = soup.find('div', class_='content').get_text()
                data_queue.put((title, content))
        except Exception as e:
            print(f"Error crawling {url}: {str(e}")

    def run(self):
        for url in self.urls:
            self.crawl_data(url)

# 消费者类，用于从队列中获取数据并存储到数据库
class Consumer(threading.Thread):
    def run(self):
        # 创建数据库连接
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 创建表格（如果不存在）
        create_table_query = """
        CREATE TABLE IF NOT EXISTS web_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT
        )
        """
        cursor.execute(create_table_query)

        while True:
            title, content = data_queue.get()
            # 将数据插入数据库
            insert_data_query = "INSERT INTO web_data (title, content) VALUES (%s, %s)"
            data = (title, content)
            cursor.execute(insert_data_query, data)
            conn.commit()
            data_queue.task_done()

# 定义要爬取的URL列表
urls_to_crawl = [
    'https://example.com/page1',
    'https://example.com/page2',
    # 添加更多的URL
]

# 创建生产者和消费者线程
producer_thread = Producer(urls_to_crawl)
consumer_thread = Consumer()

# 启动生产者和消费者线程
producer_thread.start()
consumer_thread.start()

# 等待生产者线程完成
producer_thread.join()

# 阻塞等待队列中的数据被处理完
data_queue.join()

# 停止消费者线程
consumer_thread.join()