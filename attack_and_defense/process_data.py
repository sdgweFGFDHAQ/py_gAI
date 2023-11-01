#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/13 15:11
# @Author  : zzx
# @File    : process_data.py
# @Software: PyCharm
import abc
import collections
from faker import Faker
import pandas as pd
import random

import uuid

base_columns = ['rid', 'name']
main_columns = ['CON', 'STR', 'AGI', 'SPI', 'INT', 'LUK']
sec_columns = ['HP', 'MP', 'ATN', 'ATT']


# self.rid_lists = [i for i in range(number)]
# self.name_lists = [chr(ord('a') + i) for i in range(number)]
# self.state_lists = [[random.randint(1, 10) for _ in range(len(cols) - 2)] for _ in range(number)]

# self.card = collections.namedtuple('Card', self.cols)
# self._card = [self.card(rid=rid, name=name, *state_value)
#               for rid in self.rid_lists
#               for name in self.name_lists
#               for state_value in self.state_lists]
class Card(metaclass=abc.ABCMeta):
    def __init__(self, name='xx'):
        self.rid = str(uuid.uuid4())
        self.name = name
        self.CON = random.randint(1, 10)
        self.STR = random.randint(1, 10)
        self.AGI = random.randint(1, 10)
        self.SPI = random.randint(1, 10)
        self.INT = random.randint(1, 10)
        self.LUK = random.randint(1, 10)
        self.available_points = 5
        self.HP = 20
        self.MP = 20
        self.ATN = 0
        self.ATT = 0
        self.init_sec_state()

    # 依据基础属性生成次级属性
    def init_sec_state(self):
        # 根据不同职业、不同状态设置不同的系数
        self.HP += float(self.CON * 10 + self.STR * 4)
        self.MP += float(self.AGI * 3 + self.SPI * 6)
        self.ATN += float(self.CON * 0.6 + self.STR * 1.4)
        self.ATT += float(self.AGI * 1.6 + self.SPI * 0.8)

    def generate_card(self):
        card = collections.namedtuple('Card',
                                      ['rid', 'name', 'CON', 'STR', 'AGI', 'SPI', 'INT', 'LUK', 'HP', 'MP', 'ATN',
                                       'ATT'])
        return card(rid=self.rid, name=self.name, CON=self.CON, STR=self.STR, AGI=self.AGI, SPI=self.SPI, INT=self.INT,
                    LUK=self.LUK, HP=self.HP, MP=self.MP, ATN=self.ATN, ATT=self.ATT)


def create_csv():
    fake = Faker()
    card = Card(fake.name())
    print(card.name)
    card1 = card.generate_card()
    print(card1)


if __name__ == '__main__':
    create_csv()
