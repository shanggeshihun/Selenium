# _*_coding:utf-8 _*_
# @Time　　 : 2020/1/14   1:04
# @Author　 : zimo
# @File　   :3键盘事件.py
# @Software :PyCharm
# @Theme    :
常用的键盘操作如下：

模拟键盘按键	说明
send_keys(Keys.BACK_SPACE)	删除键（BackSpace）
send_keys(Keys.SPACE)	空格键(Space)
send_keys(Keys.TAB)	制表键(Tab)
send_keys(Keys.ESCAPE)	回退键（Esc）
send_keys(Keys.ENTER)	回车键（Enter）
组合键的使用

模拟键盘按键	说明
send_keys(Keys.CONTROL,‘a’)	全选（Ctrl+A）
send_keys(Keys.CONTROL,‘c’)	复制（Ctrl+C）
send_keys(Keys.CONTROL,‘x’)	剪切（Ctrl+X）
send_keys(Keys.CONTROL,‘v’)	粘贴（Ctrl+V）
send_keys(Keys.F1…Fn)	键盘 F1…Fn