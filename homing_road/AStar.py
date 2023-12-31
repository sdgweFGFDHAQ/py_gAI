import sys
from datetime import datetime
import pygame
from pygame.font import Font
from pygame.locals import *
from pygame import time
import heapq

# 全局初始化
pygame.init()
clock = time.Clock()

# 颜色配置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 单元格尺寸
WIDTH = 25
HEIGHT = 25
# 边框粗细
MARGIN = 2
# 地图大小
ROWS = 20
COLS = 30
WINDOW_SIZE = [(MARGIN + WIDTH) * COLS + MARGIN, (MARGIN + HEIGHT) * ROWS + MARGIN]

# 默认起点和终点
START = (0, 0)
END = (ROWS - 1, COLS - 1)

# 地图网格实体
BLANK_POINT = 0
OBSTACLE_POINT = 2
START_POINT = 11
END_POINT = -11

# 定义测试状态
STATE_START = 0
STATE_HELP = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3

# 寻路状态
STOP_STATE = -1
START_STATE = 1
PAUSE_STATE = 0

prefix = "E:\\pyProjects\\py_gAI\\homing_road\\resources\\"
prefix = "./resources/"
background = pygame.transform.scale(pygame.image.load(prefix + r"city.png"),WINDOW_SIZE)
obstacle = pygame.transform.scale(pygame.image.load(prefix + r"obstacle.png"),(WIDTH, HEIGHT))
role = pygame.transform.scale(pygame.image.load(prefix + r"lxb.png"), (WIDTH, HEIGHT))
store = pygame.transform.scale(pygame.image.load(prefix + r"store.png"), (WIDTH, HEIGHT))
road = pygame.transform.scale(pygame.image.load(prefix + r"road.png"), (WIDTH, HEIGHT))


# Define the grid class
class Grid:
    def __init__(self):
        self.grid = [[0 for j in range(COLS)] for i in range(ROWS)]

    def neighbors(self, node):
        neighbors = []
        if node[0] > 0:
            neighbors.append((node[0] - 1, node[1]))
        if node[0] < ROWS - 1:
            neighbors.append((node[0] + 1, node[1]))
        if node[1] > 0:
            neighbors.append((node[0], node[1] - 1))
        if node[1] < COLS - 1:
            neighbors.append((node[0], node[1] + 1))
        return neighbors

    def cost(self, current, neighbor):
        return 1

    def draw(self, screen):
        for i in range(ROWS):
            for j in range(COLS):
                if self.grid[i][j] == BLANK_POINT:
                    # color = WHITE
                    continue
                else:
                    if self.grid[i][j] == OBSTACLE_POINT:
                        color = BLACK
                        screen.blit(obstacle, ((MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN))
                    elif self.grid[i][j] == END_POINT:
                        color = RED
                        screen.blit(store, ((MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN))
                    elif self.grid[i][j] == START_POINT:
                        color = BLUE
                        screen.blit(role, ((MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN))
                # pygame.draw.rect(screen, color,
                #                  [(MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN, WIDTH, HEIGHT])

# 定义游戏状态切换函数
def set_app_state(screen, state):
    global current_state
    current_state = state
    if current_state == STATE_START:
        # 游戏开始状态
        font = Font("C:\\Windows\\Fonts\\simkai.ttf", 28)
        text = font.render("点击空格键开始测试", True, BLACK)
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
    elif current_state == STATE_HELP:
        # 帮助状态
        font = Font(r"C:\\Windows\\Fonts\\simkai.ttf", 20)
        text = "这是一个简单的 A*算法 寻路测试\n" \
               "使用鼠标左键放置/取消障碍物\n" \
               "使用鼠标右键放置起点及终点，并可用左键取消"
        text_list = text.split("\n")
        y = 150
        for t in text_list:
            rendered_line = font.render(t, True, BLACK)
            screen.blit(rendered_line, (20, y))
            y += font.get_linesize()
    elif current_state == STATE_PLAYING:
        # 游戏进行状态
        pass
    elif current_state == STATE_GAME_OVER:
        # 游戏结束状态
        font = Font("C:\\Windows\\Fonts\\simkai.ttf", 28)
        text = font.render("测试结束，点击空格键重新开始", True, BLACK)
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)


def handle_events(grid, start, end):
    temp_game_state = game_state
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // (HEIGHT + MARGIN)
            col = pos[0] // (WIDTH + MARGIN)
            if event.button == 1:
                if grid.grid[row][col] == BLANK_POINT:
                    grid.grid[row][col] = OBSTACLE_POINT
                else:
                    if grid.grid[row][col] == OBSTACLE_POINT:
                        pass
                    if grid.grid[row][col] == START_POINT:
                        start = None
                    elif grid.grid[row][col] == END_POINT:
                        end = None
                    grid.grid[row][col] = BLANK_POINT
            elif event.button == 3:
                if start is None:
                    start = (row, col)
                    grid.grid[row][col] = START_POINT
                elif end is None and grid.grid[row][col] != START_POINT:
                    end = (row, col)
                    grid.grid[row][col] = END_POINT
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if current_state == STATE_START:
                    temp_game_state = STATE_PLAYING
                    print("{}:测试开始".format(datetime.now().strftime("%H:%M:%S")))
                elif current_state == STATE_PLAYING:
                    print("{}:测试ing".format(datetime.now().strftime("%H:%M:%S")))
                    pass
                elif current_state == STATE_GAME_OVER:
                    temp_game_state = STATE_START
                    print("{}:测试结束".format(datetime.now().strftime("%H:%M:%S")))
            elif event.key == K_h or event.unicode == u"h":
                if current_state != STATE_HELP:
                    temp_game_state = STATE_HELP
                    print("{}:查看帮助".format(datetime.now().strftime("%H:%M:%S")))
                else:
                    temp_game_state = STATE_PLAYING
                    print("{}:关闭帮助".format(datetime.now().strftime("%H:%M:%S")))
    return temp_game_state, start, end


# 曼哈顿距离
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, end, grid):
    # 初始化搜索
    open_set = [(0, start)]  # 从起点开始搜索
    closed_set = set()  # 记录已经搜索过的节点
    came_from = {}  # 记录每个节点的父节点
    g_score = {start: 0}  # 记录从起点到每个节点的实际代价
    f_score = {start: heuristic(start, end)}  # 记录从起点到每个节点的估计代价
    current = None
    turning_point = None

    while open_set:
        # 从未搜索过的节点中选择 f_score 最小的节点
        current = heapq.heappop(open_set)[1]
        # 将当前节点标记为已搜索
        closed_set.add(current)
        # 如果当前节点是终点，搜索结束
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            # 不包括 起点和终点
            try:
                path.remove(start)
                path.remove(end)
            except ValueError:
                pass
            return path
        # 对当前节点的所有邻居进行探索
        for neighbor in grid.neighbors(current):
            # 如果邻居已经被搜索过，或者是障碍物，则跳过
            if neighbor in closed_set or grid.grid[neighbor[0]][neighbor[1]] == OBSTACLE_POINT:
                continue
            # 计算从起点到邻居节点的代价
            tentative_g_score = g_score[current] + grid.cost(current, neighbor)
            # 如果邻居节点没有被搜索过，或者从起点到邻居节点的代价更小，则更新邻居节点的代价和父节点
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        if current != start and len(grid.neighbors(current)) == 1:
            if turning_point is None:
                turning_point = current
            elif current == grid.neighbors(turning_point)[0]:
                # 回溯到拐点重新开始搜索
                start = turning_point
                turning_point = None
                open_set = [(0, start)]
                came_from = {}
                g_score = {start: 0}
                f_score = {start: heuristic(start, end)}
                closed_set = set()
                break

    # 没有找到路径
    return None


def draw_path(screen, path):
    # for node in path:
    #     pygame.draw.rect(screen, GREEN,
    #                      [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN, WIDTH, HEIGHT])
    for node in path:
        screen.blit(road, ((MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN))


def main():
    # 初始化基本配置
    pygame.display.set_caption("自动寻路测试")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    grid = Grid()

    global game_state
    game_state = STATE_START
    running = False
    start = None
    end = None
    while not running:
        # 处理事件
        tgs, start, end = handle_events(grid, start, end)
        game_state = tgs
        # 绘制地图
        screen.blit(background, (0, 0))
        grid.draw(screen)
        set_app_state(screen, game_state)
        if start is not None and end is not None:
            path = astar(start, end, grid)
            if path:
                draw_path(screen, path)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
# pyinstaller --add-data 'resources:resources' -F -w -i zzx.ico AStar.py
