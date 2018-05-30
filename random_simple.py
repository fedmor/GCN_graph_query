# -*- coding: utf-8 -*-
import random


def simple_sample(graph,start,random_x,strip):
    x = random.uniform(0,1)
    visited, stack,path = set(), [start],[]
    bfs_stack = [start]
    dfs_stack = [start]
    while strip:
        if len(stack)==0: break
        if random_x > x:
            vertex = stack.pop(0)
        else:
            vertex = stack.pop()
        if vertex not in visited and vertex in graph.keys():
            path.append(vertex)
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
        x = random.uniform(0,1)
        strip-=1
    return path