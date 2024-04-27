# _*_coding:utf-8 _*_

# @Time     :2023/12/23 17:43
# @Author   :anliu
# @File     :mp4_to_ mp3.py
# @Theme    :PyCharm


from moviepy.editor import *

import ffmpeg

def extract_audio(mp4_file, mp3_file):
    ''' AudioFileClip 原mp4只有声音没有画面'''
    audio = AudioFileClip(mp4_file)
    audio.write_audiofile(mp3_file)

# 指定 MP4 文件路径和输出的 MP3 文件路径
mp4_file = "F:/MUSIC/m3u8_12/中山DjE嗦-全中文全国语慢歌连版音乐汽车音响试音必备串烧.mp4"
mp3_file = "F:/MUSIC/m3u8_12/中山DjE嗦-全中文全国语慢歌连版音乐汽车音响试音必备串烧.mp3"

extract_audio(mp4_file, mp3_file)
