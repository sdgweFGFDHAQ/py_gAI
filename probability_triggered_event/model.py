#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/6 16:46
# @Author  : zzx
# @File    : model.py
# @Software: PyCharm
# encoding=utf-8
from icecream import ic
import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class BertNet_Dialog(nn.Module):
    def __init__(self, bert_embedding, input_dim, hidden_dim, num_classes, num_layers, dropout=0.5,
                 requires_grad=False):
        super(BertLSTMNet_1, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes

        # embedding layer 线性层进行编码
        self.bert_embedding = bert_embedding
        for param in self.bert_embedding.parameters():
            param.requires_grad = requires_grad
        # 解冻后面1层的参数
        for param in self.bert_embedding.encoder.layer[-1:].parameters():
            param.requires_grad = True

        self.classifier = nn.Sequential(nn.Dropout(dropout),
                                        nn.Flatten(),
                                        nn.Linear(hidden_dim * 72, hidden_dim),
                                        nn.Linear(hidden_dim, num_classes),
                                        nn.Softmax())

    def forward(self, inputs, masks):
        inputs_bert = self.bert_embedding(input_ids=inputs, attention_mask=masks).last_hidden_state
        inputs_bert = inputs_bert.to(torch.float32)

        x = self.classifier(inputs_bert)
        return x
