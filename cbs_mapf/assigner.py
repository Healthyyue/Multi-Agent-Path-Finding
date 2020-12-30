#!/usr/bin/env python3
'''
Author: Haoran Peng
Email: gavinsweden@gmail.com
'''
from typing import List, Tuple
import numpy as np
from scipy.optimize import linear_sum_assignment

from .agent import Agent

# 这个文件两个函数的作用一致，就是为不同的车指派不同的终点。一种是用匈牙利算法进行指派，一种则是贪心搜索最近终点。

# Hungarian algorithm for global minimal cost 匈牙利算法


def min_cost(starts: List[Tuple[int, int]], goals: List[Tuple[int, int]]):
    # 断言，必须满足这个条件才进行后序操作。
    # The number of start positions must be equal to the number of goal positions
    assert(len(starts) == len(goals))

    # 定义sqdist函数，输入起点与终点。得到起点与终点：x坐标差的平方+y坐标差的平方
    def sqdist(x, y): return (x[0]-y[0])**2 + (x[1]-y[1])**2
    cost_vec = []
    # 将sqdist，利用循环一一算出每个车的起终点平方距离作为列表存储起来。
    for start in starts:
        for goal in goals:
            cost_vec.append(sqdist(start, goal))

    n = len(starts)   # n 为agent的个数，也就是starts的长度
    cost_mtx = np.array(cost_vec).reshape((n, n))   # cost_vec列表转换为矩阵（方阵）。 nXn？
    # row_ind:开销矩阵对应的行索引；col_ind:对应行索引的最优指派的列索引
    # linear_sum_assignment 是0-1规划，匈牙利算法的库函数。就出矩阵中，每一行非零值的最小值。并返回这个元素在矩阵的行列指标
    row_ind, col_ind = linear_sum_assignment(cost_mtx)

    agents = []
    # enumerate（）将括号内的列表每个元素前面加上索引序列，也就是说这个循环中i从0开始到len（starts）为止。 可以让starts除了返回元素值，还可以返回下标。（可以不从0开始）
    # 这里是将起点与终点一起加入到一个agent中， 这个 i 的引入，可以让这个工作只通过一个循环完成，否则得写两个for循环，分别append
    for i, start in enumerate(starts):
        agents.append(Agent(start, goals[col_ind[i]]))
    return agents


# Greedily choosing closest distance
def greedy_assign(starts: List[Tuple[int, int]], goals: List[Tuple[int, int]]):
    # The number of start positions must be equal to the number of goal positions
    assert(len(starts) == len(goals))

    goal_set = set(goal for goal in goals)  # 将列表goals转换为set，确保终点不重合？。
    def sqdist(x, y): return (x[0]-y[0])**2 + (x[1]-y[1])**2

    # 为每一个起点选择一个最近的终点？
    agents = []
    for start in starts:
        closest = float('inf')   # closest = 正无穷的意思
        closest_goal = None
        for goal in goal_set:
            d = sqdist(start, goal)
            if d < closest:
                closest = d
                closest_goal = goal
        goal_set.remove(closest_goal)
        agents.append(Agent(start, closest_goal))
    return agents
