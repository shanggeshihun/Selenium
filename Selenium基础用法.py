# _*_coding:utf-8 _*_

# @Time     :2023/8/13 22:09
# @Author   :anliu
# @File     :Selenium基础用法.py
# @Theme    :PyCharm

一、Selenium+Python环境搭建及配置

1.1 selenium 介绍

selenium 是一个 web 的自动化测试工具，不少学习功能自动化的同学开始首选 selenium ，因为它相比 QTP 有诸多有点：

免费，也不用再为破解 QTP 而大伤脑筋
小巧，对于不同的语言它只是一个包而已，而 QTP 需要下载安装1个多 G 的程序。
这也是最重要的一点，不管你以前更熟悉 C、 java、ruby、python、或都是 C# ，你都可以通过 selenium 完成自动化测试，而 QTP 只支持 VBS
支持多平台：windows、linux、MAC ，支持多浏览器：ie、ff、safari、opera、chrome
支持分布式测试用例的执行，可以把测试用例分布到不同的测试机器的执行，相当于分发机的功能。
1.2 selenium+Python环境配置

前提条件：已安装好Python开发环境（推荐安装Python3.5及以上版本）

安装步骤：

安装selenium
Win：pip install selenium
Mac:pip3 install selenium
安装webdriver
注：webdriver需要和对应的浏览器版本以及selenium版本对应
webdriver安装路径
Win：复制webdriver到Python安装目录下
Mac：复制webdriver到/usr/local/bin目录下
二、元素定位及浏览器基本操作

2.1 启动浏览器

2.1.1 普通方式启动

启动Chrome浏览器：

from selenium import webdriver
browser = webdriver.Chrome()
browser.get('URL')

启动Firefox浏览器：

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('URL')

启动IE浏览器：

from selenium import webdriver
browser = webdriver.Ie()
browser.get('URL')

2.1.2 Headless方式启动

Headless Chrome 是 Chrome 浏览器的无界面形态，可以在不打开浏览器的前提下，使用所有 Chrome 支持的特性运行你的程序。相比于现代浏览器，Headless Chrome 更加方便测试 web 应用，获得网站的截图，做爬虫抓取信息等。相比于较早的 PhantomJS，SlimerJS 等，Headless Chrome 则更加贴近浏览器环境。

Headless Chrome 对Chrome版本要求：
官方文档中介绍，mac和linux环境要求chrome版本是59+，而windows版本的chrome要求是60+，同时chromedriver要求2.30+版本。

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless') //增加无界面选项
chrome_options.add_argument('--disable-gpu') //如果不加这个选项，有时定位会出现问题
# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "URL"
browser.get(mainUrl)
print(f"browser text = {browser.page_source}")
browser.quit()

2.1.3 加载配置启动浏览器

Selenium操作浏览器是不加载任何配置的，下面是关于加载Chrome配置的方法：

用Chrome地址栏输入chrome://version/，查看自己的“个人资料路径”，然后在浏览器启动时，调用这个配置文件，代码如下：

#coding=utf-8
from selenium import webdriver
option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data') #设置成用户自己的数据目录
driver=webdriver.Chrome(chrome_options=option)

而加载Firefox配置的方法有些不同：

打开Firefox点右上角设置>？（帮助）>故障排除信息>显示文件夹，打开后把路径复制下来就可以了

# coding=utf-8
from selenium import webdriver
# 配置文件地址
profile_directory = r'C:\Users\\xxx\AppData\Roaming\Mozilla\Firefox\Profiles\1x41j9of.default'
# 加载配置配置
profile = webdriver.FirefoxProfile(profile_directory)
# 启动浏览器配置
driver = webdriver.Firefox(profile)

2.2 元素定位

对象的定位应该是自动化测试的核心，要想操作一个对象，首先应该识别这个对象。一个对象就是一个人一样，他会有各种的特征（属性），如比我们可以通过一个人的身份证号，姓名，或者他住在哪个街道、楼层、门牌找到这个人。那么一个对象也有类似的属性，我们可以通过这个属性找到这对象。

webdriver 提供了一系列的对象定位方法，常用的有以下几种：

id定位：find_element_by_id()
name定位：find_element_by_name()
class定位：find_element_by_class_name()
link定位：find_element_by_link_text()
partial link定位：find_element_by_partial_link_text()
tag定位：find_element_by_tag_name()
xpath定位：find_element_by_xpath()
css定位：find_element_by_css_selector()
#coding=utf-8
from selenium import webdriver
browser=webdriver.Firefox()
browser.get("URL")
#########百度输入框的定位方式##########
#通过id方式定位
browser.find_element_by_id("kw").send_keys("selenium")
#通过name方式定位
browser.find_element_by_name("wd").send_keys("selenium")
#通过tag name方式定位
browser.find_element_by_tag_name("input").send_keys("selenium")
#通过class name方式定位
browser.find_element_by_class_name("s_ipt").send_keys("selenium")
#通过CSS方式定位
browser.find_element_by_css_selector("#kw").send_keys("selenium")
#通过xpath方式定位
browser.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")
############################################
browser.find_element_by_id("su").click()
time.sleep(3)
browser.quit()

2.2.1 class含有空格时解决方法：

在实际进行元素定位时，经常发现class name是有多个class组合的复合类，中间以空格隔开。如果直接进行定位会出现报错，可以通过以下方式处理：

class属性唯一但是有空格，选择空格两边唯一的那一个
若空格隔开的class不唯一可以通过索引进行定位
self.driver.find_elements_by_class_name('table-dragColumn')[0].click()
通过css方法进行定位（空格以‘.’代替）
#前面加（.）空格地方用点（.）来代替
self.driver.find_element_by_css_selector('.dtb-style-1.table-dragColumns').click()
#包含整个类
self.driver.find_element_by_css_selector('class="dtb-style-1 table-dragColumns').click()

参考代码：

# coding:utf-8
from selenium import webdriver
driver = webdriver.Firefox()
driver.get("URL")
driver.implicitly_wait(20)
driver.switch_to.frame("x-URS-iframe")
# 方法一：取单个class属性
driver.find_element_by_class_name("dlemail").send_keys("yoyo")
driver.find_element_by_class_name("dlpwd").send_keys("12333")
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

2.3 selenium三种等待方式

有时候为了保证脚本运行的稳定性，需要脚本中添加等待时间。

2.3.1 强制等待

第一种也是最简单粗暴的一种办法就是强制等待sleep(xx)，需要引入“time”模块，这种叫强制等待，不管你浏览器是否加载完了，程序都得等待3秒，3秒一到，继续执行下面的代码，作为调试很有用，有时候也可以在代码里这样等待，不过不建议总用这种等待方式，太死板，严重影响程序执行速度。

# -*- coding: utf-8 -*-
from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get('URL')
time.sleep(3) # 强制等待3秒再执行下一步
print(driver.current_url)
driver.quit()

2.3.2 隐性等待

第二种办法叫隐性等待，通过添加 implicitly_wait() 方法就可以方便的实现智能等待；implicitly_wait(30) 的用法应该比 time.sleep() 更智能，后者只能选择一个固定的时间的等待，前者可以 在一个时间范围内智能的等待。

# -*- coding: utf-8 -*-
from selenium import webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(30) # 隐性等待，最长等30秒
driver.get('URL')
print(driver.current_url)
driver.quit()

隐形等待是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。注意这里有一个弊端，那就是程序会一直等待整个页面加载完成，也就是一般情况下你看到浏览器标签栏那个小圈不再转，才会执行下一步，但有时候页面想要的元素早就在加载完成了，但是因为个别js之类的东西特别慢，我仍得等到页面全部完成才能执行下一步，我想等我要的元素出来之后就下一步怎么办？有办法，这就要看selenium提供的另一种等待方式——显性等待wait了。
需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可，我曾看到有人把隐性等待当成了sleep在用，走哪儿都来一下…

2.3.3 显性等待

第三种办法就是显性等待，WebDriverWait，配合该类的until()和until_not()方法，就能够根据判断条件而进行灵活地等待了。它主要的意思就是：程序每隔xx秒看一眼，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException。

wait模块的WebDriverWait类是显性等待类，先看下它有哪些参数与方法：

selenium.webdriver.support.wait.WebDriverWait（类）

init

driver: 传入WebDriver实例，即我们上例中的driver
timeout: 超时时间，等待的最长时间（同时要考虑隐性等待时间）
poll_frequency: 调用until或until_not中的方法的间隔时间，默认是0.5秒
ignored_exceptions: 忽略的异常，如果在调用until或until_not的过程中抛出这个元组中的异常，则不中断代码，继续等待，如果抛出的是这个元组外的异常，则中断代码，抛出异常。默认只有NoSuchElementException。

until

method: 在等待期间，每隔一段时间（__init__中的poll_frequency）调用这个传入的方法，直到返回值不是False
message: 如果超时，抛出TimeoutException，将message传入异常

until_not

与until相反，until是当某元素出现或什么条件成立则继续执行，
until_not是当某元素消失或什么条件不成立则继续执行，参数也相同，不再赘述。

看了以上内容基本上很清楚了，调用方法如下：

WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)

这里需要特别注意的是until或until_not中的可执行方法method参数，很多人传入了WebElement对象，如下：

WebDriverWait(driver, 10).until(driver.find_element_by_id('kw')) # 错误

这是错误的用法，这里的参数一定要是可以调用的，即这个对象一定有 call() 方法，否则会抛出异常：

TypeError: 'xxx' object is not callable

在这里，你可以用selenium提供的 expected_conditions 模块中的各种条件，也可以用WebElement的 is_displayed() 、is_enabled()、**is_selected() **方法，或者用自己封装的方法都可以。

#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
base_url = "URL"
driver = webdriver.Firefox()
driver.implicitly_wait(5)
'''隐式等待和显示等待都存在时，超时时间取二者中较大的'''
locator = (By.ID,'kw')
driver.get(base_url)
WebDriverWait(driver,10).until(EC.title_is(u"百度一下，你就知道"))
'''判断title,返回布尔值'''
WebDriverWait(driver,10).until(EC.title_contains(u"百度一下"))
'''判断title，返回布尔值'''
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'kw')))
'''判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement'''
WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'su')))
'''判断某个元素是否被添加到了dom里并且可见，可见代表元素可显示且宽和高都大于0'''
WebDriverWait(driver,10).until(EC.visibility_of(driver.find_element(by=By.ID,value='kw')))
'''判断元素是否可见，如果可见就返回这个元素'''
WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.mnav')))
'''判断是否至少有1个元素存在于dom树中，如果定位到就返回列表'''
WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.mnav')))
'''判断是否至少有一个元素在页面中可见，如果定位到就返回列表'''
WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,"//*[@id='u1']/a[8]"),u'设置'))
'''判断指定的元素中是否包含了预期的字符串，返回布尔值'''
WebDriverWait(driver,10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,'#su'),u'百度一下'))
'''判断指定元素的属性值中是否包含了预期的字符串，返回布尔值'''
#WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it(locator))
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
print instance.text
instance.accept()
driver.close()

2.4 浏览器操作

2.4.1 浏览器最大化、最小化

将浏览器最大化显示

browser.maximize_window()

将浏览器最小化显示

browser.minimize_window()

2.4.2 浏览器设置窗口大小

设置浏览器宽480、高800显示

browser.set_window_size(480, 800)

2.4.3 浏览器前进后退

前进

browser.forword()

后退

browser.back()

2.5 操作测试对象

一般来说，webdriver 中比较常用的操作对象的方法有下面几个：

click——点击对象
send_keys——在对象上模拟按键输入
clear——清除对象的内容，如果可以的话
submit——提交对象的内容，如果可以的话
text——用于获取元素的文本信息
2.6 键盘事件

要想调用键盘按键操作需要引入 keys 包：from selenium.webdriver.common.keys import Keys通过 send_keys()调用按键：send_keys(Keys.TAB) # TABsend_keys(Keys.ENTER) # 回车

参考代码：

#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #需要引入 keys 包
import os,time
driver = webdriver.Firefox()
driver.get("http://passport.kuaibo.com/login/?referrer=http%3A%2F%2Fwebcloud .kuaibo.com%2F")
time.sleep(3)
driver.maximize_window() # 浏览器全屏显示
driver.find_element_by_id("user_name").clear()
driver.find_element_by_id("user_name").send_keys("fnngj")
#tab 的定位相相于清除了密码框的默认提示信息，等同上面的 clear()
driver.find_element_by_id("user_name").send_keys(Keys.TAB)
time.sleep(3)
driver.find_element_by_id("user_pwd").send_keys("123456")
#通过定位密码框，enter（回车）来代替登陆按钮
driver.find_element_by_id("user_pwd").send_keys(Keys.ENTER)
#也可定位登陆按钮，通过 enter（回车）代替 click()
driver.find_element_by_id("login").send_keys(Keys.ENTER)
time.sleep(3)
driver.quit()

键盘组合键的用法：

#ctrl+a 全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')

#ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')

2.7 鼠标事件

鼠标事件一般包括鼠标右键、双击、拖动、移动鼠标到某个元素上等等。
需要引入ActionChains类。
引入方法：
from selenium.webdriver.common.action_chains import ActionChains

ActionChains 常用方法：
perform() 执行所有ActionChains 中存储的行为；
context_click() 右击；
double_click() 双击；
drag_and_drop() 拖动；
move_to_element() 鼠标悬停。

鼠标双击示例：

#定位到要双击的元素
qqq =driver.find_element_by_xpath("xxx")
#对定位到的元素执行鼠标双击操作
ActionChains(driver).double_click(qqq).perform()

鼠标拖放示例：

#定位元素的原位置
element = driver.find_element_by_name("source")
#定位元素要移动到的目标位置
target = driver.find_element_by_name("target")
#执行元素的移动操作
ActionChains(driver).drag_and_drop(element, target).perform()

2.8 多层框架/层级定位

定位元素过程中经常会遇到找不到元素的问题，出现该问题一般都是以下因素导致：

元素定位方法不对
页面存在iframe或内嵌窗口
页面超时
webdriver 提供了一个 switch_to_frame 方法，可以很轻松的来解决这个问题。
用法：

#先找到到 ifrome1（id = f1）
browser.switch_to_frame("f1")

同样的，如果是内嵌窗口：
browser.switch_to_window("f1")

2.9 Expected Conditions解析

Expected Conditions的使用场景有2种：

直接在断言中使用
与WebDriverWait配合使用，动态等待页面上元素出现或者消失
相关方法：

title_is: 判断当前页面的title是否精确等于预期
title_contains： 判断当前页面的title是否包含预期字符串
presence_of_element_located：判断某个元素是否被加到了dom树里，并不代表该元素一定可见
visibility_of_element_located：判断某个元素是否可见.可见代表元素非隐藏，并且元素的宽和高都不等于0
visibility_of：跟上面的方法做一样的事情，只是上面的方法要传入locator，这个方法直接传定位到的element就好了
presence_of_all_elements_located：判断是否至少有1个元素存在于dom树中。举个例子，如果页面上有n个元素的class都是'column-md-3'，那么只要有1个元素存在，这个方法就返回True
text_to_be_present_in_element：判断某个元素中的text是否包含了预期的字符串
text_to_be_present_in_element_value：判断某个元素中的value属性是否包含了预期的字符串
frame_to_be_available_and_switch_to_it：判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False
invisibility_of_element_located：判断某个元素中是否不存在于dom树或不可见
element_to_be_clickable：判断某个元素中是否可见并且是enable的，这样的话才叫clickable
staleness_of：等某个元素从dom树中移除，注意，这个方法也是返回True或False
element_to_be_selected：判断某个元素是否被选中了,一般用在下拉列表
element_selection_state_to_be：判断某个元素的选中状态是否符合预期
element_located_selection_state_to_be：跟上面的方法作用一样，只是上面的方法传入定位到的element，而这个方法传入locator
alert_is_present：判断页面上是否存在alert，这是个老问题，很多同学会问到
示例：
判断title：title_is()、title_contains()

首先导入expected_conditions模块
由于这个模块名称比较长，所以为了后续的调用方便，重新命名为EC了（有点像数据库里面多表查询时候重命名）
打开博客首页后判断title,返回结果是True或False
# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.get("URL")
# 判断title完全等于
title = EC.title_is(u'冰封')
print title(driver)
# 判断title包含
title1 = EC.title_contains(u'冰封')
print title1(driver)
# 另外一种写法
r1 = EC.title_is(u'冰封')(driver)
r2 = EC.title_contains(u'冰封')(driver)
print r1
print r2

三、Selenium速查表

3.1 Python Webdriver Exception速查表

webdriver在使用过程中可能会出现各种异常，我们需要了解该异常并知道如何进行异常处理。

异常 描述

WebDriverException 所有webdriver异常的基类，当有异常且不属于下列异常时抛出 InvalidSwitchToTargetException 下面两个异常的父类，当要switch的目标不存在时抛出 NoSuchFrameException 当你想要用switch_to.frame()切入某个不存在的frame时抛出 NoSuchWindowException 当你想要用switch_to.window()切入某个不存在的window时抛出 NoSuchElementException 元素不存在，一般由find_element与find_elements抛出 NoSuchAttributeException 一般你获取不存在的元素属性时抛出，要注意有些属性在不同浏览器里是有不同的属性名的 StaleElementReferenceException 指定的元素过时了，不在现在的DOM树里了，可能是被删除了或者是页面或iframe刷新了 UnexpectedAlertPresentException 出现了意料之外的alert，阻碍了指令的执行时抛出 NoAlertPresentException 你想要获取alert，但实际没有alert出现时抛出 InvalidElementStateException 下面两个异常的父类，当元素状态不能进行想要的操作时抛出 ElementNotVisibleException 元素存在，但是不可见，不可以与之交互 ElementNotSelectableException 当你想要选择一个不可被选择的元素时抛出 InvalidSelectorException 一般当你xpath语法错误的时候抛出这个错 InvalidCookieDomainException 当你想要在非当前url的域里添加cookie时抛出 UnableToSetCookieException 当driver无法添加一个cookie时抛出 TimeoutException 当一个指令在足够的时间内没有完成时抛出 MoveTargetOutOfBoundsException actions的move操作时抛出，将目标移动出了window之外 UnexpectedTagNameException 获取到的元素标签不符合要求时抛出，比如实例化Select，你传入了非select标签的元素时 ImeNotAvailableException 输入法不支持的时候抛出，这里两个异常不常见，ime引擎据说是仅用于linux下对中文/日文支持的时候 ImeActivationFailedException 激活输入法失败时抛出 ErrorInResponseException 不常见，server端出错时可能会抛 RemoteDriverServerException 不常见，好像是在某些情况下驱动启动浏览器失败的时候会报这个错

3.2 Xpath&Css定位方法速查表

描述 Xpath

Css

直接子元素 //div/a div > a

子元素或后代元素 //div//a div a

以id定位 //div[@id='idValue']//a div#idValue a

以class定位 //div[@class='classValue']//a div.classValue a

同级弟弟元素 //ul/li[@class='first']/following- ul>li.first + li 属性 //form/input[@name='username'] form input[name='username'] 多个属性 //input[@name='continue' and input[name='continue'][type='button

第4个子元素 //ul[@id='list']/li[4] ul#list li:nth-child(4)

第1个子元素 //ul[@id='list']/li[1] ul#list li:first-child

最后1个子元素 //ul[@id='list']/li[last()] ul#list li:last-child

属性包含某字段 //div[contains(@title,'Title')] div[title*="Title"]

属性以某字段开头 //input[starts-with(@name,'user')] input[name^="user"]

属性以某字段结尾 //input[ends-with(@name,'name')] input[name$="name"]

text中包含某字段 //div[contains(text(), 'text')]

无法定位 元素有某属性 //div[@title] div[title]

父节点 //div/.. 无法定位