#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/30 11:25
# @Author  : zzx
# @File    : zlj.py
# @Software: PyCharm
import random
import time

import requests
import re

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
txt_path = "mushroom.txt"
title = ''


def get_all_content():
    # with open(txt_path, 'w', encoding='utf-8') as f:
    #     f.write('')
    print("======启动======")

    prefix = "https://www.weiquxs.net"
    suffix = "/xiaoshuo/44907/9836269_2.html"
    while True:
        try:
            # 主功能
            url = prefix + suffix
            print("--url: ", url)
            suffix = get_session(url)
        except Exception as e:
            print("!----!error!----!\n", e)
            break
    print("======完成======")


def get_session(url):
    # 写文件
    file_name = open(txt_path, 'a', encoding='utf-8')
    session = requests.Session()
    try:
        time.sleep(random.uniform(1, 3))
        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'
        response.raise_for_status()
        print("--response: ", response)
        # 主功能
        next_suffix = get_paging_content(response, file_name=file_name)
        return next_suffix

    except requests.exceptions.RequestException as e:
        print('Error occurred(session):', e)
    finally:
        session.close()
        file_name.close()


def get_paging_content(response, file_name):
    global title
    # 获取文本名
    name = re.findall(r'<meta name="keywords" content="(.*?)">', response.text)[0]
    name = str(name).split(',')[0]
    if title != name:
        title = name
        file_name.write(title)
        file_name.write('\n')
    print("--name: ", name)

    # 获取文本内容
    chapters = re.findall(r'<div id="content">(.*?)</div>', response.text, re.S)[0]
    chapters = chapters.replace(' ', '')
    chapters = chapters.replace('()', '')
    chapters = chapters.replace('& lt;!--go - - & gt;', '')
    chapters = chapters.replace('&lt;!--go--&gt;', '')
    # 转换字符串
    s = str(chapters)
    s_replace = s.replace('</p>', "\n")
    while True:
        index_begin = s_replace.find("<")
        index_end = s_replace.find(">", index_begin + 1)
        if index_begin == -1 or index_end == -1:
            break
        s_replace = s_replace.replace(s_replace[index_begin:index_end + 1], "")
    pattern = re.compile(r'&nbsp;', re.I)
    fiction = pattern.sub(' ', s_replace)
    file_name.write(fiction)
    file_name.write('\n')

    # 获取下一个
    next_path = re.findall(r'<a rel="next" href="(.*?)">', response.text)[0]
    print("--next_path: ", next_path)
    return str(next_path)


if __name__ == '__main__':
    get_all_content()
