# _*_coding:utf-8 _*_

#@Time      : 2021/12/22  11:39
#@Author    : An
#@File      : test_recursion.py
#@Software  : PyCharm

"""
python中递归深度是有限制的。一般默认为999，当超过999时，会出现错误：RuntimeError: maximum recursion depth exceeded while calling a Python object

解决方法为手工设置递归调用深度：
import sys
sys.setrecursionlimit(1000000)  # 例如这里设置为一百万
"""
import sys
sys.setrecursionlimit(10000)

def fib(n):
    if n == 1:
        return 1
    else:
        return fib(n-1) + n
if __name__ == '__main__':
    fib(1000)