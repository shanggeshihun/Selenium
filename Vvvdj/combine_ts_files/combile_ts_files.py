# _*_coding:utf-8 _*_

# @Time     :2023/11/19 12:45
# @Author   :anliu
# @File     :combile_ts_files.py
# @Theme    :将多个ts文件合并


import os


# 步骤1：找到所有待合并的TS文件

# 指定TS文件所在目录
directory = "./ts_files"
# 获取目录中的所有文件
files = [f for f in os.listdir(directory) if f.endswith(".ts")]

# 步骤2：按照文件名的顺序将TS文件合并

# 对文件列表进行排序
files = sorted(files)

# 打开新文件用于保存合并后的内容
with open("merged.ts", "wb") as outfile:
    # 逐个读取TS文件并写入到新文件中
    for filename in files:
        with open(os.path.join(directory, filename), "rb") as infile:
            outfile.write(infile.read())

# 步骤3：将合并后的TS文件保存为一个完整的视频文件
import subprocess
# 使用ffmpeg将TS文件转换为MP4格式
subprocess.call(["ffmpeg", "-i", "merged.ts", "output.mp4"])

