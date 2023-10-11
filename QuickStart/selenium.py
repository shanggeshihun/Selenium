# coding:utf-8
# --- 2.1.1 普通方式启动 ---
from selenium import  webdriver
browser=webdriver.Chrome()
url='http://www.baidu.com'


# --- Headless方式启动 ---
from selenium import webdriver
browser=webdriver.Chrome()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

chrome_options=webdriver.ChromeOptions()
# 使用headless无界面浏览器模型
# chrome_options.add_argument('--headless') # 增加无界面选项
# chrome_options.add_argument('--disable-gpu')# 如果不加这个选项，有时定位会出问题

# 启动浏览器，获取网页源代码
# chrome://version/
browser=webdriver.Chrome(chrome_options=chrome_options)
main_url='http://www.taobao.com/'
browser.get(main_url)
page_source=(browser.page_source)
print(type(page_source))
print(page_source)
browser.quit()


# --- 元素定位 ---
from selenium import webdriver
browser=webdriver.Chrome()
url='http://www.baidu.com/'
browser.get(url)
# === 百度输入框的定位方式
# 通过id方式定位
browser.find_element_by_id('kw').send_keys('selenium')
# 通过name方式定位
browser.find_element_by_name('wd').send_keys('selenium')
# 通过tag name方式定位
browser.find_element_by_tag_name("input").send_keys('selenium')
# 通过css方式定位
browser.find_element_by_css_selector('#kw').send_keys('selenium')
# 通过xpath方式定位
browser.find_element_by_xpath("//input[@id='kw']").send_keys('selenium')
# === 百度提交的定位方式
browser.find_element_by_id('su').click()
time.sleep(3)
browser.quit()



"""
class含有空格时解决方法：
在实际进行元素定位时，经常发现class name是有多个class组合的复合类，中间以空格隔开。如果直接进行定位会出现报错，可以通过以下方式处理：

class属性唯一但是有空格，选择空格两边唯一的那一个
若空格隔开的class不唯一可以通过索引进行定位
self.driver.find_elements_by_class_name('table-dragColumn')[0].click()
通过css方法进行定位（空格以‘.’代替）
\
"""
from selenium import webdriver
driver=webdriver.Chrome()
url='https://mail.126.com/'
driver.get(url)
driver.implicitly_wait(20)

# 方法一：取单个class属性
driver.find_element_by_class_name('dlemail').send_keys('yoyo')
driver.find_element_by_class_name('dlpwd').send_keys('12333')

# 方法二：定位一组取下标定位（乃下策）
driver.find_elements_by_class_name("j-inputtext")[0].send_keys("yoyo")
driver.find_elements_by_class_name("j-inputtext")[1].send_keys("12333")

# 方法三：css定位
driver.find_element_by_css_selector(".j-inputtext.dlemail").send_keys("yoyo")
driver.find_element_by_css_selector(".j-inputtext.dlpwd").send_keys("123")

# 方法四：取单个class属性也是可以的
driver.find_element_by_css_selector(".dlemail").send_keys("yoyo")
driver.find_element_by_css_selector(".dlpwd").send_keys("123")

# 方法五：直接包含空格的CSS属性定位大法
driver.find_element_by_css_selector("[class='j-inputtext dlemail']").send_keys("yoyo")



"""
2.3 selenium三种等待方式
有时候为了保证脚本运行的稳定性，需要脚本中添加等待时间。

2.3.1 强制等待
第一种也是最简单粗暴的一种办法就是强制等待sleep(xx)，需要引入“time”模块，这种叫强制等待，不管你浏览器是否加载完了，程序都得等待3秒，3秒一到，继续执行下面的代码，作为调试很有用，有时候也可以在代码里这样等待，不过不建议总用这种等待方式，太死板，严重影响程序执行速度。
"""
"""
2.3.2 隐性等待
第二种办法叫隐性等待，通过添加 implicitly_wait() 方法就可以方便的实现智能等待；implicitly_wait(30) 的用法应该比 time.sleep() 更智能，后者只能选择一个固定的时间的等待，前者可以 在一个时间范围内智能的等待。
"""
from selenium import webdriver
driver=webdriver.Chrome()
driver.implicitly_wait(30) # 隐形等待，最长等待30秒
url='http://www.baidu.com/'
driver.get(url)
driver.quit()
"""
隐形等待是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。注意这里有一个弊端，那就是程序会一直等待整个页面加载完成，也就是一般情况下你看到浏览器标签栏那个小圈不再转，才会执行下一步，但有时候页面想要的元素早就在加载完成了，但是因为个别js之类的东西特别慢，我仍得等到页面全部完成才能执行下一步，我想等我要的元素出来之后就下一步怎么办？有办法，这就要看selenium提供的另一种等待方式——显性等待wait了。
需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可，我曾看到有人把隐性等待当成了sleep在用，走哪儿都来一下…
"""
"""2.3.3 显性等待"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
base_url='http://www.baidu.com/'
driver=webdriver.Chrome()
driver.implicitly_wait(5)
'''隐式等待和显示等待都存在时，超时时间取二者中较大的'''
driver.get(base_url)

WebDriverWait(driver,10).until(EC.title_is('百度一下，你就知道'))
'''判断title,返回布尔值'''

WebDriverWait(driver,10).until(EC.title_contains('百度一下'))
'''判断title，返回布尔值'''

WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'kw')))
'''判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement'''

# WebDriverWait(driver,10).until(EC.invisibility_of_element_located((By.ID,'su'))) # 报错
'''判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0'''

WebDriverWait(driver,10).until(EC.visibility_of(driver.find_element(by=By.ID,value='kw')))
'''判断元素是否可见，如果可见就返回这个元素'''

WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.mnav')))
'''判断是否至少有1个元素存在于dom树中，如果定位到就返回列表'''

WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.mnav')))
'''判断是否至少有一个元素在页面中可见，如果定位到就返回列表'''

WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,"//*[@id='u1']/a[8]"),u'设置')) # 报错
'''判断指定的元素中是否包含了预期的字符串，返回布尔值'''

WebDriverWait(driver,10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,'#su'),u'百度一下'))
'''判断指定元素的属性值中是否包含了预期的字符串，返回布尔值'''

# WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it(locator))
'''判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False'''
#注意这里并没有一个frame可以切换进去

WebDriverWait(driver,10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR,'#swfEveryCookieWrap')))
'''判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素'''
#注意#swfEveryCookieWrap在此页面中是一个隐藏的元素


WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='u1']/a[8]"))).click()
'''判断某个元素中是否可见并且是enable的，代表可点击'''
driver.find_element_by_xpath("//*[@id='wrapper']/div[6]/a[1]").click()
#WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='wrapper']/div[6]/a[1]"))).click()

#WebDriverWait(driver,10).until(EC.staleness_of(driver.find_element(By.ID,'su')))
'''等待某个元素从dom树中移除'''
#这里没有找到合适的例子

WebDriverWait(driver,10).until(EC.element_to_be_selected(driver.find_element(By.XPATH,"//*[@id='nr']/option[1]")))
'''判断某个元素是否被选中了,一般用在下拉列表'''

WebDriverWait(driver,10).until(EC.element_selection_state_to_be(driver.find_element(By.XPATH,"//*[@id='nr']/option[1]"),True))
'''判断某个元素的选中状态是否符合预期'''

WebDriverWait(driver,10).until(EC.element_located_selection_state_to_be((By.XPATH,"//*[@id='nr']/option[1]"),True))
'''判断某个元素的选中状态是否符合预期'''
driver.find_element_by_xpath(".//*[@id='gxszButton']/a[1]").click()

instance = WebDriverWait(driver,10).until(EC.alert_is_present())
'''判断页面上是否存在alert,如果有就切换到alert并返回alert的内容'''
print(instance.text)
instance.accept()


# 将浏览器最大化显示
driver.maximize_window()

# 将浏览器最小化显示
driver.minimize_window()

# 设置浏览器宽480、高800显示
driver.set_window_size(480, 800)

# 前进
driver.forward()

# 后退
driver.back()
driver.close()

'''
2.5 操作测试对象
一般来说，webdriver 中比较常用的操作对象的方法有下面几个：

click——点击对象
send_keys——在对象上模拟按键输入
clear——清除对象的内容，如果可以的话
submit——提交对象的内容，如果可以的话
text——用于获取元素的文本信息
'''
from pandas import read
'''
2.5 操作测试对象
一般来说，webdriver 中比较常用的操作对象的方法有下面几个：

click——点击对象
send_keys——在对象上模拟按键输入
clear——清除对象的内容，如果可以的话
submit——提交对象的内容，如果可以的话
text——用于获取元素的文本信息
'''
'''
要想调用键盘按键操作需要引入 keys 包：
from selenium.webdriver.common.keys import Keys通过 send_keys()调用按键：
send_keys(Keys.TAB) # TAB
send_keys(Keys.ENTER) # 回车
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,time
driver=webdriver.Chrome()
driver.get('http://www.baidu.com/')
time.sleep(2)
driver.maximize_window()




