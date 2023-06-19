import pygame
from pygame.locals import *


def drow_windows():
    """
    1.使用pygame.image.load()加载图像的数据
    2.使用游戏屏幕对象，调用blit方法将图像绘制到指定位置
    3.调用pygame.display.update()方法更新屏幕的显示
    """
    pygame.init()

    # 创建游戏的窗口 480*700
    screen = pygame.display.set_mode((480, 700), 0, 0)

    # 绘制背景图像
    background = pygame.image.load("./shoot/background.png")
    screen.blit(background, (0, 0))

    # 绘制大飞机
    bigplane = pygame.image.load("./shoot/hero0.png")
    screen.blit(bigplane, (200, 500))

    # 统一更新
    pygame.display.update()

    while True:
        # 为当前窗口增加事件
        # 利用pygame注册事件，其返回值是一个列表
        # 存放当前注册时获取的所有事件
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    pygame.quit()

if __name__ == '__main__':
    drow_windows()