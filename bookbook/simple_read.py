#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/14 17:05
# @Author  : zzx
# @File    : simple_read.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
import logging
import os
import sys

import codecs
from datetime import datetime
import platform
import re

import pandas as pd

"""
一个txt文件存储所有章节
根据 第x章 去划分文本
"""


def generate_onlyTXT():
    # 设置文件夹路径
    folder_path = "./contents"

    # 获取文件夹下所有的 TXT 文件名
    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    # 遍历每个 TXT 文件并修改文件名
    for index, file_name in enumerate(txt_files):
        if not re.search(r'第.章', file_name):
            # 获取旧文件名的完整路径
            old_file_path = os.path.join(folder_path, file_name)

            # 修改文件名
            number = "第{}章".format(index + 1)
            new_file_name = file_name.replace(file_name, number + ' ' + file_name)  # 根据需要修改文件名的规则
            new_file_path = os.path.join(folder_path, new_file_name)

            # 重命名文件
            os.rename(old_file_path, new_file_path)

    # 获取文件夹下所有的 TXT 文件名
    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    # 创建一个用于保存所有文件内容的新 TXT 文件
    output_file_path = "SkyrimV.txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        # 遍历每个 TXT 文件并将内容写入新文件
        for file in txt_files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "r", encoding="utf-8") as input_file:
                output_file.write(file)
                output_file.write(input_file.read())

    print("文件处理完成！")


class Reader:
    def __init__(self, book_name, txt_path):
        self.book_name = book_name
        self.txt_path = txt_path
        self.contents = []  # 章节名称
        self.book = self.split_book_chapter()

    def split_book_chapter(self):
        """
        读取文本文件，并将文本按章节划分
        :param txt_path:
        :return:
        """
        book_content = {}

        with codecs.open(self.txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

            chapters = re.split("\n===第.{1,6}章===", text)
            i = 1

            for chapter in chapters:
                title = "第{}章".format(i)
                text = chapter.split("\n")
                text = "\n".join(text)
                book_content[title] = text
                i += 1

        self.contents = list(book_content.keys())
        return book_content

    def get_index(self, key_name):
        """
        根据书的章节名称，获取前一章与后一章
        :param key_name:
        :return:
        """
        this_index = self.contents.index(key_name)
        last_chapter = self.contents[this_index - 1]
        next_chapter = self.contents[this_index + 1]
        return last_chapter, next_chapter

    def start_read(self, chapter_name="第1章"):
        """
        开始阅读, 章节名称为空，且数据库中没有历史记录时，从第一章开始
        :param chapter_name: 章节名称
        :return:
        """
        chapter_name = chapter_name[0] if isinstance(chapter_name, tuple) else chapter_name

        read_content = "".join(self.book.get(chapter_name, "当前章节不存在"))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("chapter_name", chapter_name)
        text_list = read_content.split('\n')
        for text in text_list:
            limitation = 100
            if len(text) > limitation:
                text = '\n'.join([text[i:i + limitation] for i in range(0, len(text), limitation)])
            print(text)
            print("last_chapter = self.contents[this_index - 1]"
                  "next_chapter = self.contents[this_index + 1]"
                  "if platform.system().lower() == 'linux':os.system('clear')\n")
            print(
                "==== AUTHENTICATION FAILED ===\n"
                "Failed to start docker.service: Access denied\n"
                "See system logs and 'systemctl status docker.service' for details.")

        forward = ""
        while forward not in ["n", "b", "q"]:
            forward = input("""n、下一章\nb、上一章\nq、退出""")

        last_chapter_name, next_chapter_name = self.get_index(chapter_name)
        if forward == "q":
            sys.exit(0)
        # 根据命令选择上一章或者下一章，并更新历史记录
        if forward == "n":
            return next_chapter_name
        if forward == "b":
            return last_chapter_name


def start_read():
    mybook = Reader("415", "aaa.txt")
    chapter_name = "第51章"
    while True:
        if platform.system().lower() == "windows":
            os.system('cls')
        if platform.system().lower() == "linux":
            os.system('clear')
        chapter_name = mybook.start_read(chapter_name)


def more_simple_read(path="./contents/第287章 费福根卷1.txt"):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # 去除行末尾的换行符和空白字符
            limitation = 80
            if len(line) > limitation:
                line = '\n'.join([line[i:i + limitation] for i in range(0, len(line), limitation)])
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(line)
            print("last_chapter = self.contents[this_index - 1]"
                  "next_chapter = self.contents[this_index + 1]"
                  "if platform.system().lower() == 'linux':os.system('clear')"
                  "mybook.start_read(chapter_name)")


def print_lines(path='aaaa.txt', current_chapter=60):
    with open(path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        lines_per_batch = 500
        total_line = len(lines)
        current_line = current_chapter * lines_per_batch

        while current_line < total_line:
            print("======{},{}======".format(current_chapter, current_line))
            batch = lines[current_line:current_line + lines_per_batch]
            for line in batch:
                line = line.strip()  # 去除行末尾的换行符和空白字符
                limitation = 80
                if len(line) > limitation:
                    line = "\n[[0.4781, 0.4168, 0.6548, 0.4341, 0.4870, 0.3478, 0.7284, 0.5700, 0.4740],\n" \
                           "[0.6982, 0.5589, 0.6166, 0.6952, 0.4532, 0.5158, 0.2362, 0.3328, 0.5992]]\n\n" \
                           "last_chapter = self.contents[this_index - 1];" \
                           "next_chapter = self.contents[this_index + 1]\n" \
                           "if platform.system().lower() == 'linux':os.system('clear')\n\n" \
                           "<class 'numpy.ndarray'>\n<class 'numpy.ndarray'>\n\n" \
                           "precision: 89.81%,recall: 95.20%,F1:91.65% | precision: 96.16%,recall: 98.06%,F1:96.77%\n" \
                           "%Y-%m-%d %H:%M:%S next_chapter = self.contents[this_index + 1]\n\n"\
                        .join([line[i:i + limitation] for i in range(0, len(line), limitation)])
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print(line)
                print("last_chapter = self.contents[this_index - 1]"
                      "next_chapter = self.contents[this_index + 1]"
                      "if platform.system().lower() == 'linux':os.system('clear')"
                      "mybook.start_read(chapter_name)")

            user_input = input("按下字母键 'n' 并回车")
            if user_input.lower() == 'n':
                current_chapter += 1
                current_line += lines_per_batch
            elif user_input.lower() == 'b':
                current_chapter -= 1
                current_line -= lines_per_batch
                if current_chapter < 0:
                    current_chapter = 0
                    current_line = 0
            else:
                break


if __name__ == '__main__':
    # generate_onlyTXT()
    # more_simple_read()

    # start_read()

    print_lines()
