# _*_coding:utf-8 _*_

#@Time      : 2021/12/17  13:37
#@Author    : An
#@File      : 单线程.py
#@Software  : PyCharm

from selenium import webdriver

class LianJia:
    def __init__(self):
        # 声明Chrome浏览器对象, 这里填写你自己的driver路径
        self.driver = webdriver.Chrome(r'E:\chromedriver.exe')

    def house_detail(self, item):
        """获取一间房子的详情信息"""
        self.driver.get(item['houseURL'])  # 访问一间房子的详情页
        # 获取页面上的房子信息
        item['title'] = self.driver.find_element_by_tag_name('h1').text    # 标题
        item['price'] = self.driver.find_element_by_css_selector('span.total').text    # 价格
        house_info = self.driver.find_elements_by_css_selector('div.mainInfo')
        item['room'] = house_info[0].text    # 户型
        item['faceTo'] = house_info[1].text   # 朝向
        item['area'] = house_info[2].text     # 面积
        # 小区名
        item['communityName'] = self.driver.find_element_by_css_selector('div.communityName a.info').text
        # 发布日期
        item['releaseDate'] = self.driver.find_element_by_xpath('//div[@class="transaction"]/div[2]/ul/li/span[2]').text
        print(item)

    def house_list(self, item):
        """获取一个城区中所有房子的详情页链接"""
        # 访问城区的页面
        self.driver.get(item['partURL'])
        # 切换到'最新发布'页面
        self.driver.find_element_by_link_text('最新发布').click()
        # 获取到所有的房子链接
        house_ls = self.driver.find_elements_by_xpath('//ul[@class="sellListContent"]//div[@class="title"]/a')
        # 生成url列表
        house_url_ls = [house.get_attribute("href") for house in house_ls]
        # 遍历房子的链接
        for url in house_url_ls:
            item['houseURL'] = url
            self.house_detail(item)

    def run(self):
        """获取所有城区的页面链接"""
        # 访问二手房网址
        self.driver.get('https://wh.lianjia.com/ershoufang/')
        # 获取所有城区的元素对象
        temp_ls = self.driver.find_elements_by_xpath('//div[@class="position"]/dl[2]/dd/div[1]/div/a')
        # 城区名
        part_name_ls = [ele.text for ele in temp_ls]
        # 城区链接
        part_url_ls = [ele.get_attribute("href") for ele in temp_ls]
        item = {}   # 初始化一个容器, 用来存放房子的信息
        for i in range(len(temp_ls)):
            item['partName'] = part_name_ls[i]    # 城区名
            item['partURL'] = part_url_ls[i]    # 城区页面链接
            self.house_list(dict(item))    # 传递深拷贝的item对象

if __name__ == '__main__':
    lj = LianJia() # 输入希望爬取的页数
    lj.run()