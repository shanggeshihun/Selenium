# _*_coding:utf-8 _*_

# @Time     :2023/12/23 20:59
# @Author   :anliu
# @File     :mp4_to_mp3_2.py
# @Theme    :PyCharm


import os
import glob
import queue
import threading
import subprocess
from moviepy.editor import *

input_folder = r'F:\MUSIC\m3u8_12'
output_folder = r'F:\MUSIC\m3u8_12_mp3'

def func(input_file, output_file):
    audio = AudioFileClip(input_file)
    audio.write_audiofile(output_file)

def convert_file():
    while True:
        input_file = q.get()
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp3')
        func(input_file, output_file)
        q.task_done()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

input_files = glob.glob(os.path.join(input_folder, '*.mp4'))

q = queue.Queue()

num_threads = 4  # 指定线程数量

# 启动线程
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=convert_file)
    t.start()
    threads.append(t)

# 将文件路径放入队列
for input_file in input_files:
    q.put(input_file)

# 等待队列中的所有任务完成
q.join()

# 停止线程
for t in threads:
    t.join()

print("All files processed.")