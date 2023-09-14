#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/12 15:02
# @Author  : zzx
# @File    : keras_flask.py.py
# @Software: PyCharm

import base64
from flask import Flask, render_template, request
from imageio import imread, imsave
from PIL import Image
import tensorflow as tf
import numpy as np
import re
from tensorflow.keras.models import load_model
from tensorflow.python.keras.backend import set_session
import logging

logging.basicConfig(filename="keras_flask.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)

# 1. 初始化 flask app
app = Flask(__name__)

# 2. 初始化global variables
sess = tf.Session()
graph = tf.get_default_graph()


# 3. 将用户画的图输出成output.png
def convertImage(imgData1):
    imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))


# 4. 搭建前端框架
@app.route('/')
def index():
    return render_template("index.html")


# 5. 定义预测函数
@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    # 这个函数会在用户点击‘predict’按钮时触发
    # 会将输出的output.png放入模型中进行预测
    # 同时在页面上输出预测结果
    logging.info("接收图片")
    imgData = request.get_data()
    convertImage(imgData)
    # 读取图片
    logging.info("读取图片")
    x = imread('output.png', pilmode='L')
    # 设置图片的规格
    x = np.array(Image.fromarray(x).resize((28, 28))) / 255
    # 可以保存最终处理好的图片
    logging.info("保存图片")
    imsave('final_image.jpg', x)
    x = x.reshape(1, 28, 28, 1)

    # 调用训练好的模型和并进行预测
    global graph
    global sess
    with graph.as_default():
        set_session(sess)
        model = load_model('model.h5')
        out = model.predict(x)
        logging.info("当前预测结果:{}".format(out))
        response = np.argmax(out, axis=1)
        logging.info("返回结果")
        return str(response[0])


# 6. 返回本地访问地址
if __name__ == "__main__":
    # 让app在本地运行，定义了host和port
    app.run(host='0.0.0.0', port=5000)
