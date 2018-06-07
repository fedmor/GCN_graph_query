# -*- coding: utf-8 -*-
# from DT_index import paserData
# import Graph
import numpy as np
import itertools

import time


def get_join_order(matching_result, query_graph, query_matching_vtx):
    freq_vtxs = [0] * len(matching_result)
    for index in range(len(matching_result)):
        match_result = np.array(matching_result[index])
        freq = np.sum(match_result)
        freq_vtxs[index] = freq
    vtx_value = [0] * len(matching_result)
    for index in range(len(matching_result)):
        id = query_matching_vtx[index]
        freq_vtx = freq_vtxs[index]
        vtx_out_dregee = len(query_graph[id])
        value = float(vtx_out_dregee) / freq_vtx
        vtx_value[index] = value
    join_order = np.argsort(-np.array(vtx_value))

    return join_order


def get_node_index(v):
    index = []
    for i in range(len(v)):
        if v[i] == 1:
            index.append(i)
    return index


def bfs(head_vtx, query_graph):
    graph = query_graph
    visited, queue = set(), [head_vtx]
    path = []
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            path.append(vertex)
            try:
                extend_list = graph[vertex] - visited
            except:
                extend_list = []
            queue.extend(extend_list)
    return path


# def get_join_order(queryVtxs, queryEdges, query_graph):
#     query_graph_martix = [[0] * len(queryVtxs)] * len(queryVtxs)
#     for edge in queryEdges:
#         query_graph_martix[edge[0]][edge[1]] = 1
#     b = np.array(query_graph_martix).T
#     head_vtx = 0
#     for i in range(len(b)):
#         if np.sum(b[i]) == 0:
#             head_vtx = 0
#     join_order = bfs(head_vtx, query_graph)
#     return join_order


def joinProcess(oneRst, Chds, matching_children_label, Chd_label_count):
    match_result_label_vtx = {}
    for i in range(len(Chds)):
        vtx = Chds[i]
        label = matching_children_label[i]
        if label in Chd_label_count.keys():
            if label not in match_result_label_vtx.keys():
                match_result_label_vtx[label] = [vtx]
            else:
                match_result_label_vtx[label].append(vtx)

    frist = True
    permutations = []

    for key, value in match_result_label_vtx.iteritems():

        if frist:
            n = len(Chd_label_count[key])
            for i in itertools.permutations(value, n):
                item = {key: [j for j in i]}
                permutations.append(item)
            frist = False
        else:
            n = len(Chd_label_count[key])
            per = list(itertools.permutations(value, n))

            product = list(itertools.product(per, permutations))
            new_permutations = []
            for i in product:
                item = i[1]
                item[key] = [j for j in i[0]]
                new_permutations.append(item)
            permutations = new_permutations

    partitionRst = []
    for per in permutations:
        tmpRst = []
        tmpRst.extend(oneRst)

        for key, Chds in Chd_label_count.iteritems():
            matchvalue = per[key]
            for i in range(len(Chds)):
                if tmpRst[Chds[i]] == -1:
                    tmpRst[Chds[i]] = matchvalue[i]
                else:
                    if tmpRst[Chds[i]] != matchvalue[i]:
                        continue
            # try:
            #     matchvalue = per[key]
            #     for i in range(len(Chds)):
            #         if tmpRst[Chds[i]] == -1:
            #             tmpRst[Chds[i]] = matchvalue[i]
            #         else:
            #             if tmpRst[Chds[i]] != matchvalue[i]:
            #                 continue
            # except:
            #     print("permutations", permutations)
            #     print("per, ", per)
            #     print("key, ", key)

        partitionRst.append(tmpRst)
    return partitionRst


"""
Funtion: frist_join
par: match_result_vtx_Chd: match result of vtx, include it's Chd
par: vtx: matching vtx
par: Chd_label_count: vtx's Chd count of label
par: data_vtx_label: data graph vtx -> label
par: q_vtx_children: vtx of qury data children
"""


def frist_join(match_result_vtx_Chd, index, root_vtx, Chd_label_count, data_vtx_label, q_vtx_count, query_vtx_label):
    frist_matchs = match_result_vtx_Chd[root_vtx]  # dict
    partitionRst = []

    for root in frist_matchs:
        Chds = frist_matchs[root]
        matching_children_label = [data_vtx_label[Chd] for Chd in Chds]
        no_sub_stru = False

        if data_vtx_label[root] != query_vtx_label: continue  # label_unequal

        match_label_count = {}
        for i in range(len(Chds)):
            # vtx = Chds[i]
            label = matching_children_label[i]
            if label in match_label_count.keys():
                match_label_count[label] += 1
            else:
                match_label_count[label] = 1
        for label in Chd_label_count:
            if label in match_label_count.keys():
                if match_label_count[label] < len(Chd_label_count[label]):
                    no_sub_stru = True
            else:
                no_sub_stru = True
        if no_sub_stru: continue

        oneRst = [-1] * q_vtx_count
        # print("oneRst: ",len(oneRst))
        # print("root: ",vtx)
        oneRst[root_vtx] = root

        # try:
        #     oneRst[vtx] = root
        # except:
        #     print(root)
        #     print(oneRst)
        #     time.sleep(10000000)
        oneRst = joinProcess(oneRst, Chds, matching_children_label, Chd_label_count)
        partitionRst.extend(oneRst)
    return partitionRst


def next_join(partJoinedGraph, match_result_vtx_Chd, index, root_vtx, Chd_label_count, data_vtx_label, q_vtx_children,
              query_vtx_label):
    match_results = match_result_vtx_Chd[root_vtx]
    partitionRst = []
    for perRst in partJoinedGraph:
        for root in match_results:

            Chds = match_results[root]
            matching_children_label = [data_vtx_label[Chd] for Chd in Chds]

            no_sub_stru = False
            if data_vtx_label[root] != query_vtx_label: continue  # label_unequal

            match_label_count = {}
            for i in range(len(Chds)):
                # vtx = Chds[i]
                label = matching_children_label[i]
                if label in match_label_count.keys():
                    match_label_count[label] += 1
                else:
                    match_label_count[label] = 1
            for label in Chd_label_count:
                if label in match_label_count.keys():
                    if match_label_count[label] < len(Chd_label_count[label]):
                        no_sub_stru = True
                else:
                    no_sub_stru = True
            if no_sub_stru: continue

            if perRst[root_vtx] == -1:
                peredChd = [perRst[children] for children in q_vtx_children]
                children_is_Rst = False
                for i in peredChd:
                    if i != -1:
                        children_is_Rst = True
                if children_is_Rst:
                    Chds = match_results[root]
                    is_parent = False
                    for Chd in Chds:
                        if Chd in peredChd:
                            is_parent = True
                    if is_parent:
                        # Chds = match_results[root]
                        # matching_children_label = [data_vtx_label[Chd] for Chd in Chds]
                        perRst[root_vtx] = root
                        oneRst = joinProcess(perRst, Chds, matching_children_label, Chd_label_count)
                        partitionRst.extend(oneRst)
                    else:
                        continue

            else:
                if root == perRst[root_vtx]:
                    # Chds = match_results[root]
                    # matching_children_label = [data_vtx_label[Chd] for Chd in Chds]
                    oneRst = joinProcess(perRst, Chds, matching_children_label, Chd_label_count)
                    partitionRst.extend(oneRst)
                else:
                    continue
    return partitionRst


def join(join_order, query_matching_vtx, match_result_vtx, graph, query_graph, query_vtx_label, data_vtx_label):
    # query_vtx_label = {item[0]: item[1] for item in queryVtxs[0]}
    # data_vtx_label = {item[0]: item[1] for item in dataVtx[0]}
    match_result_vtx_Chd = {}
    match_vtxs_sum = []
    have_children_no_match = False
    for index in range(len(match_result_vtx)):
        root = query_matching_vtx[index]
        one_pattern = {}
        if len(match_result_vtx[index]) == 0: have_children_no_match = True
        for vtx in range(len(match_result_vtx[index])):
            if match_result_vtx[index][vtx] == 1:
                try:
                    Chd = list(graph[vtx])
                except:
                    Chd = []
                one_pattern[vtx] = Chd
                match_vtxs_sum.append(vtx)
        match_result_vtx_Chd[root] = one_pattern
    match_vtxs_set = set(match_vtxs_sum)

    if len(match_vtxs_set) < len(query_vtx_label): return []
    if have_children_no_match: return []

    frist_run = True
    frist_head = []
    partJoinedGraph = []
    for index in join_order:
        vtx = query_matching_vtx[index]
        q_vtx_children = query_graph[vtx]
        vtx_children_map = {Chd: query_vtx_label[Chd] for Chd in q_vtx_children}

        Chd_label_count = {}
        for key, value in vtx_children_map.iteritems():
            if value not in Chd_label_count.keys():
                Chd_label_count[value] = [key]
            else:
                Chd_label_count[value].append(key)

        if frist_run:
            partJoinedGraph = frist_join(match_result_vtx_Chd, index, vtx, Chd_label_count, data_vtx_label,
                                         len(query_vtx_label), query_vtx_label[vtx])
            frist_run = False
        else:
            partJoinedGraph = next_join(partJoinedGraph, match_result_vtx_Chd, index, vtx, Chd_label_count,
                                        data_vtx_label,
                                        q_vtx_children, query_vtx_label[vtx])
        if len(partJoinedGraph)==0:
            return partJoinedGraph
    return partJoinedGraph

# v0 = [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 1., 0., 1., 0., 1., 0., 0.]
# v1 = [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 1., 0., 1., 0., 1., 0., 0.]
# v2 = [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 1., 0., 1., 0., 1., 0., 0.]
# v3 = [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 1., 0., 1., 0., 1., 0., 0.]
# v4 = [1., 1., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
#
# datafilePath = "./data/sample/dataset"
# queryfilePath = "./data/sample/Q4"
#
# dataVtx, dataEdge, label_set = paserData(datafilePath)
# queryVtxs, queryEdges, q_label_set = paserData(queryfilePath)
#
# graph = Graph.Graph(dataEdge[0])
# query_graph = Graph.Graph(queryEdges[0])
#
# query_vtx_label = {item[0]: item[1] for item in queryVtxs[0]}
# data_vtx_label = {item[0]: item[1] for item in dataVtx[0]}
#
# match_result_vtx = [get_node_index(v) for v in [v0, v1, v2, v3, v4]]
# match_result_vtx_Chd = {}
# for root in range(len(match_result_vtx)):
#     childens = {}
#     for vtx in match_result_vtx[root]:
#         try:
#             Chd = list(graph[vtx])
#         except:
#             Chd = []
#         childens[vtx] = Chd
#     match_result_vtx_Chd[root] = childens
#
# join_order = get_join_order(queryVtxs[0], queryEdges[0], query_graph)
# # print(join_order)
#
# frist_run = True
# frist_head = []
# partJoinedGraph=[]
# for vtx in join_order[:-1]:
#
#     q_vtx_children = query_graph[vtx]
#     vtx_children_map = {Chd: query_vtx_label[Chd] for Chd in q_vtx_children}
#
#     Chd_label_count = {}
#     for key, value in vtx_children_map.iteritems():
#         if value not in Chd_label_count.keys():
#             Chd_label_count[value] = [key]
#         else:
#             Chd_label_count[value].append(key)
#
#     if frist_run:
#         partJoinedGraph = frist_join(match_result_vtx_Chd, vtx, Chd_label_count, data_vtx_label, q_vtx_children)
#         frist_run = False
#     else:
#         partJoinedGraph = next_join(partJoinedGraph, match_result_vtx_Chd, vtx, Chd_label_count, data_vtx_label,
#                                     q_vtx_children)
# print partJoinedGraph
