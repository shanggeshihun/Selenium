# _*_coding:utf-8 _*_

# @Time     :2023/11/19 13:03
# @Author   :anliu
# @File     :m3u8_release_to_ts.py
# @Theme    :PyCharm

import sys, requests
m3u8_url = 'https://tspc.vvvdj.com/c2/2023/11/259632-773da6/259632.m3u8?upt=f509d9f01703001599'
m3u8_name = m3u8_url.split('?')[0].split('/')[-1].split('.')[0]

headers = {
    'Referer': 'https://www.vvvdj.com/',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
response = requests.get(url=m3u8_url, headers=headers, verify=False)
if response.status_code == 200:
    # /{} E盘根目录，./{}当前文件夹，../m3u8_release_to_ts/{}.m3u8 当前文件夹
    with open(r'./{}.m3u8'.format(m3u8_name), "wb") as fp:
        fp.write(response.content)

# 实际上 resonse_content 即 就记录ts文件

print(response.content) # 二进制
print('response.content vs response.text')
print(response.text) # 文本

ts_list = []
for line in response.text.readlins():
    if '#EXTINF' in line:
        continue
    ts_list.append(line)

