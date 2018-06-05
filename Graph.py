# -*- coding: utf-8 -*-
def Graph(edges):
    graph = {}
    for edge in edges:
        if edge[0] in graph.keys():
            graph[edge[0]].add(edge[1])
        else:
            graph[edge[0]] = set([edge[1]])
    return graph

# def Graph(edges,vtxs):
#     graph = {}
#
#     for edge in edges:
#         if edge[0] in graph.keys():
#             graph[edge[0]].add(edge[1])
#         else:
#             graph[edge[0]] = set([edge[1]])
#     return graph