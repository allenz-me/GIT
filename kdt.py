from math import sqrt
from statistics import variance, median_high
from collections import namedtuple
from copy import deepcopy

import random
import matplotlib.pyplot as plt

class Point:
    __point = namedtuple('Point', 'x y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.__tuple = Point.__point(self.x, self.y)

    def __repr__(self):
        return str(self.__tuple)

    __str__ = __repr__



class KDTNode:

    def __init__(self, p: Point, split, left=None, right=None):
        self.p = p
        self.split = split
        self.left = left
        self.right = right


class KDTree:

    def __init__(self, points):
        self.__points = points
        varX = variance([getattr(i, 'x') for i in points])
        varY = variance([getattr(i, 'y') for i in points])
        split = 'x' if varX > varY else 'y'
        self.__head = KDTree.generate(points, split)

    @staticmethod
    def generate(points, split) -> KDTNode:
        if len(points) == 0:
            return None
        elif len(points) == 1:
            return KDTNode(points[0], split)
        f = lambda x: getattr(x, split)
        data = sorted(points, key=f)
        index = int(len(data)/2) # middle right
        p = data[index]
        node = KDTNode(p, split)
        leftData = data[0:index]
        rightData = data[index+1:]
        split = 'x' if split == 'y' else 'y'
        node.left = KDTree.generate(leftData, split)
        node.right = KDTree.generate(rightData, split)
        return node
    
    @staticmethod
    def distance(p1:Point, p2:Point):
        return sqrt( (p1.x - p2.x)**2 + (p1.y - p2.y)**2 ) 

    def nearest(self, x:float, y:float) -> Point:
        p = Point(x, y)
        # 首先找到(x,y)对应的叶子节点
        node = self.__head
        path = []
        while node is not None:
            path.append(node)
            cmp = x if node.split == 'x' else y
            if cmp > getattr(node.p, node.split):
                node = node.right
            else:
                node = node.left
        
        path_copy = deepcopy(path)
        # path保存了寻找叶子节点所经过的路径节点
        dist = KDTree.distance(path[-1].p, p)
        r = [dist, path[-1].p] # 暂时的最短组合, r[0]保存了最短距离
        # 回溯查找
#         plt.figure(figsize=(6,6))
#         k = 0
#         plt.scatter([getattr(p, 'x') for p in self.__points],[getattr(p,'y') for p in self.__points],c='black',s=5)
        while len(path) != 0:
            back_p = path.pop()
            if back_p is None:
                continue
#             plt.scatter([back_p.p.x], [back_p.p.y], s=12)
#             k += 1
            dist = KDTree.distance(back_p.p, p)
            if dist < r[0]:
                r[0], r[1] = dist, back_p.p
            split = back_p.split
            diff = getattr(back_p.p, split) - getattr(p, split)
            if abs(diff) <= r[0]: # 如果与分割线相交
                if diff <= 0:
                    path.append(back_p.left)
                if diff >= 0:
                    path.append(back_p.right)
            elif back_p not in path_copy:
                push = back_p.right if diff < 0 else back_p.left # 刚好与上面的if语句相反
                path.append(push)
                
#         plt.scatter([r[1].x], [r[1].y],c='blue',s=20)
#         plt.legend([''] + [str(i) for i in range(1, k+1)], bbox_to_anchor=(1.2, 1))
#         plt.scatter([x], [y], marker='D', c="red", s=20)
#         plt.xlim(-10, 10)
#         plt.ylim(-10, 10)
#         plt.savefig('/data/jupyter/1.jpg', dpi=800)
        return r[1]