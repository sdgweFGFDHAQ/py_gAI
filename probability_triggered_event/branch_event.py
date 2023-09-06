import random


def minCostClimbingStairs(cost):
    p = c =0
    for i in range(2, len(cost) + 1):
        n = min(c + cost[i - 1], p + cost[i - 2])
        p, c = c, n
    return c


def ad(n):
    c = {}
    c[1] = 1
    c[2] = 2
    for i in range(3, n + 1):
        c[i] = c[i - 1] + c[i - 2]
    print(c[n])

if __name__ == '__main__':
    cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    result = minCostClimbingStairs(cost)
    print(result)
