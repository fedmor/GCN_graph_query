# -*- coding: utf-8 -*-
import json
import random


from Graph import Graph
from random_simple import simple_sample


def bfs(graph, start):
    visited, queue = set(), [start]
    path = []
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            path.append(vertex)
            queue.extend(graph[vertex] - visited)
    return path


def match(query_kernel, cnn_dg):
    value = 0
    for i in range(len(query_kernel)):
        if query_kernel[i] == cnn_dg[i]:
            value += 1
    return value


def main():
    vtx_file = open('./data/wordNet/wordnet_vertexes.txt')
    edge_file = open('./data/wordNet/wordnet_edges.txt')
    vtx_query = open('./data/wordNet/vtx_query_10.txt')
    edges_query = open('./data/wordNet/edge_query_10.txt')

    vtxs_map = {}
    edges = []
    while True:
        line = vtx_file.readline().strip("\n")
        d = line.split(" ")
        if not line: break
        if d[0] not in vtxs_map:
            vtxs_map[int(d[0])] = int(d[1])

    while True:
        line = edge_file.readline().strip("\n")
        d = line.split(" ")
        if not line: break
        edges.append([int(d[0]), int(d[1])])
        edges.append([int(d[1]), int(d[0])])

    graph = Graph(edges)

    # query graph
    query_vtxs_map = {}
    query_edges = []
    while True:
        line = vtx_query.readline().strip("\n")
        d = line.split(" ")
        if not line: break
        if d[0] not in vtxs_map:
            query_vtxs_map[int(d[0])] = int(d[1])

    while True:
        line = edges_query.readline().strip("\n")
        d = line.split(" ")
        if not line: break
        query_edges.append([int(d[0]), int(d[1])])
        query_edges.append([int(d[1]), int(d[0])])
    query_graph = Graph(query_edges)

    # 获取查询图bfs编码
    query_bfs = {}
    for vtx in query_vtxs_map.keys():
        bfs_path = bfs(query_graph, vtx)
        label_vector = [query_vtxs_map.get(i) for i in bfs_path[1:]]
        query_bfs[vtx] = label_vector
    print("完成查询图的映射")

    # for item in query_bfs.items():
    #     print item
    # 获取数据图bfs编码
    vtxs_bfs = {}
    for vtx in vtxs_map.keys():
        for i in range(5):
            if i == 0:
                bfs_path = simple_sample(graph, vtx, 0.4, 10)
                if len(bfs_path) > 9:
                    label_vector = [vtxs_map.get(i) for i in bfs_path[1:]]
                    vtxs_bfs[vtx] = [label_vector]
                else:
                    vtxs_bfs[vtx] = []
            else:
                bfs_path = simple_sample(graph, vtx, 0.4, 10)
                if len(bfs_path) > 9:
                    label_vector = [vtxs_map.get(i) for i in bfs_path[1:]]
                    vtxs_bfs[vtx].append(label_vector)
    print("完成数据图的映射")

    print("开始匹配")
    match_result = {}
    for q_key, q_value in query_bfs.iteritems():
        match_vtx_7 = []
        match_vtx_8 = []
        match_vtx_9 = []
        for d_key, d_values in vtxs_bfs.iteritems():
            for d_value in d_values:
                value = match(q_value, d_values)
                if value > 7: match_vtx_7.append(d_key)
                if value > 8: match_vtx_8.append(d_key)
                if value > 9: match_vtx_9.append(d_key)
        match_result[q_key] = [match_vtx_7, match_vtx_8, match_vtx_9]

    for key,values in match_result.iteritems():
        print("vtx id : %i , match value 7 number:%i, match value 8 number:%i, match value 9 number:%i"%(key,len(values[0]),len(values[1]),len(values[2])))

    jsObj = json.dumps(match_result)

    fileObject = open('./result/result.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

    # query_kernels = []
    # query_vtx = []
    # for item in query_bfs.items():
    #     label_vector = [query_vtxs_map.get(i) for i in item[1][1:]]
    #     query_vtx.append(item[0])
    #     query_kernels.append(label_vector)


if __name__ == '__main__':
    main()
