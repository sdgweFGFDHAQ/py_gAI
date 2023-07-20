import pygame
from pygame.locals import *
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


# 曼哈顿距离
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, end, grid):
    # Initialize the open and closed sets
    open_set = [(0, start)]  # priority queue of nodes to explore
    closed_set = set()  # set of nodes already explored
    came_from = {}  # dictionary of nodes mapping to their parent nodes
    g_score = {start: 0}  # cost of the path from start to a given node
    f_score = {start: heuristic(start, end)}  # estimated total cost from start to end through a given node

    while open_set:
        # Get the node with the lowest f_score
        current = heapq.heappop(open_set)[1]

        # If we have reached the end, reconstruct the path and return it
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Otherwise, add the current node to the closed set and explore its neighbors
        closed_set.add(current)
        for neighbor in grid.neighbors(current):
            # If the neighbor has already been explored, skip it
            if neighbor in closed_set:
                continue

            # Calculate the cost of the path from start to the neighbor through the current node
            tentative_g_score = g_score[current] + grid.cost(current, neighbor)

            # If the neighbor is not in the open set or the new path to it is cheaper than the previous one, update its scores
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If we have explored all nodes and haven't found the end, return an empty path
    return []


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
                if self.grid[i][j] == 1:
                    color = BLACK
                elif self.grid[i][j] == -1:
                    color = RED
                elif self.grid[i][j] == -2:
                    color = BLUE
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN, WIDTH, HEIGHT])


def main():
    # 初始化基本配置
    pygame.init()
    WINDOW_SIZE = [(MARGIN + WIDTH) * COLS + MARGIN, (MARGIN + HEIGHT) * ROWS + MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("自动寻路测试")
    grid = Grid()
    start = None
    end = None

    # 开始寻路
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            # 鼠标点击响应设置障碍
            elif event.type == MOUSEBUTTONDOWN:
                # mouse click
                pos = pygame.mouse.get_pos()
                row = pos[1] // (HEIGHT + MARGIN)
                col = pos[0] // (WIDTH + MARGIN)
                # 左键设置
                if event.button == 1:
                    grid.grid[row][col] = 1
                # 右键取消
                elif event.button == 3:
                    if grid.grid[row][col] == -2:
                        start = None
                    elif grid.grid[row][col] == -1:
                        end = None
                    grid.grid[row][col] = 0
                # 中键设置起点和终点
                elif event.button == 2:
                    if start is None:
                        start = (row, col)
                        grid.grid[row][col] = -2
                    elif end is None:
                        end = (row, col)
                        grid.grid[row][col] = -1
            # 如果起点和终点设置好了, 开始运行自动寻路并绘制
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if start is not None and end is not None:
                        path = astar(start, end, grid)
                        for node in path:
                            pygame.draw.rect(screen, GREEN,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH,
                                              HEIGHT])

        grid.draw(screen)
        # 刷新频率
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
