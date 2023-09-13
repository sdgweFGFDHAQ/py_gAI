#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/6 16:44
# @Author  : zzx
# @File    : ai_main.py
# @Software: PyCharm
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def dialog():
    # 加载预训练的 GPT 模型和分词器
    model_name = 'gpt2'  # 或者使用 'gpt2-medium' 或 'gpt2-large'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # 设置生成的参数
    max_length = 50  # 生成文本的最大长度
    num_return_sequences = 5  # 生成多个候选序列
    temperature = 0.7  # 控制生成文本的多样性，值越大越随机

    # 输入对话的开头文本
    input_text = "玩家: 你好，NPC:"

    # 对输入文本进行分词和编码
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # 使用模型生成文本
    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature
        )

    # 解码生成的文本并打印
    for i, generated_text in enumerate(output):
        text = tokenizer.decode(generated_text, skip_special_tokens=True)
        print(f"候选序列 {i+1}: {text}")


if __name__ == '__main__':
    dialog()
