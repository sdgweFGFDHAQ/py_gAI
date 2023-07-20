import pygame
from pygame.locals import *
from pygame import time
import heapq

# 颜色配置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 单元格尺寸
WIDTH = 20
HEIGHT = 20
# 边框粗细
MARGIN = 2

# 地图大小
ROWS = 20
COLS = 20

# 默认起点和终点
START = (0, 0)
END = (ROWS - 1, COLS - 1)

# 地图网格实体
BLANK_POINT = 0
OBSTACLE_POINT = 2
START_POINT = 11
END_POINT = -11

# 寻路状态
STOP_STATE = -1
START_STATE = 1
PAUSE_STATE = 0


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
                color = WHITE
                if self.grid[i][j] == OBSTACLE_POINT:
                    color = BLACK
                elif self.grid[i][j] == END_POINT:
                    color = RED
                elif self.grid[i][j] == START_POINT:
                    color = BLUE
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN, WIDTH, HEIGHT])


def handle_events(grid, start, end):
    game_state = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
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
                elif end is None:
                    end = (row, col)
                    grid.grid[row][col] = END_POINT
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if start is not None and end is not None:
                    game_state = True
    return game_state, start, end


def draw_path(screen, path):
    for node in path:
        pygame.draw.rect(screen, GREEN,
                         [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN, WIDTH, HEIGHT])


def main():
    # 初始化基本配置
    pygame.init()
    clock = time.Clock()
    WINDOW_SIZE = [(MARGIN + WIDTH) * COLS + MARGIN, (MARGIN + HEIGHT) * ROWS + MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("自动寻路测试")
    grid = Grid()

    done = False
    start = None
    end = None
    while not done:
        # 处理事件
        game_state, start, end = handle_events(grid, start, end)
        # 绘制地图
        grid.draw(screen)
        if start is not None and end is not None:
            path = astar(start, end, grid)
            if path:
                draw_path(screen, path)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
