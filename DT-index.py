# -*- coding: utf-8 -*-
import Graph
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
import graphviz
import pydotplus
from sklearn import tree
from IPython.display import Image
import os

def paserData(datafilePath):
    vtx = {}
    edge = {}
    label_set = []
    graphId = -1
    data = open(datafilePath)
    while True:
        line = data.readline().strip("\n")
        if not line: break
        if "#" in line:
            id = line.split(" ")[-1]
            graphId = int(id)
            if graphId not in vtx:
                vtx[graphId] = []
            if graphId not in edge:
                edge[graphId] = []
        if "v" in line:
            item = line.split(" ")[1:]
            vtx_item = [int(i) for i in item]
            vtx[graphId].append(vtx_item)
            label_set.append(vtx_item[1])
            if vtx_item[1] == 51:
                print(graphId)
                print(vtx_item)
        if "e" in line:
            item = line.split(" ")[1:]
            edge_item = [int(i) for i in item]
            edge[graphId].append(edge_item)
    return vtx, edge, set(label_set)


def coding_label(label_set):
    label_list = list(label_set)
    label_map = {}
    for label in label_set:
        coding = [0] * len(label_set)
        coding[label_list.index(label)] = 1
        label_map.update({label: coding})
    return label_map


def get_graph_neb(edges, vtxs):
    vtxs = [vtx[0] for vtx in vtxs]
    graph = {}.fromkeys(vtxs)
    for vtx in vtxs:
        graph[vtx] = []
    for edge in edges:
        graph[edge[0]].append(edge[1])
    return graph


def get_abj_coding(neb_nodes, label_codes, vtxs_label):
    coding_list = [0] * len(label_codes[0])
    for node in neb_nodes:
        node_label = vtxs_label[node]
        node_code = label_codes[node_label]
        for i in range(len(coding_list)):
            coding_list[i] = coding_list[i] + node_code[i]
    return coding_list


def get_node_Eigenvalues(vtx_id, graph, n):
    seq_list = [vtx_id]
    nodes_set = [vtx_id]
    sub_graph = {}
    while n:
        tmp_nodes = []
        for node in seq_list:
            adj_node = list(graph[node])
            tmp_nodes.extend(adj_node)
            nodes_set.extend(adj_node)
            sub_graph[node] = adj_node
        seq_list = tmp_nodes
        n -= 1
    node_nub = len(nodes_set)
    adj_matrix = [[0] * node_nub] * node_nub
    for vtx in sub_graph.keys():
        i = nodes_set.index(vtx)
        adj_node = sub_graph[vtx]
        for node in adj_node:
            adj_matrix[i][nodes_set.index(node)] = 1
    R = np.array(adj_matrix)
    a, b = np.linalg.eig(R)
    a = sorted(a,reverse=True)
    if len(a) <2: a.append(0.0)
    return a


def find_max_vtxs(dataVtx):
    max_vtx_mub = 0
    id = 0
    for key,value in dataVtx.iteritems():
        if max_vtx_mub<len(value):
            id = key
            max_vtx_mub = len(value)
    return id,max_vtx_mub
    pass


def paser_DT(id, vtx_nub, graph_vtxs_coding):
    graph_0 = graph_vtxs_coding[id]
    Y = [i[0] for i in graph_0]
    X = []
    for item in graph_0:
        tmp = []
        for i in range(1, len(item)):
            tmp.extend(item[i])
        X.append(tmp)
    a = [len(i) for i in X]
    model_tree = DecisionTreeClassifier()
    model_tree.fit(X, Y)
    dot_data = tree.export_graphviz(model_tree, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph_name = "ID_%s.pdf"%(str(id))
    graph.write_pdf('./DT-PDF/'+graph_name)
    pass


def main():
    datafilePath = "./data/sample/dataset"
    dataVtx, dataEdge, label_set = paserData(datafilePath)
    label_codes = coding_label(label_set)
    graph_vtxs_coding = {}
    for key in dataVtx.keys():
        vtxs_coding = []
        vtxs = dataVtx[key]
        edges = dataEdge[key]
        vtxs_label = {vtx[0]: vtx[1] for vtx in vtxs}
        neb_dict = get_graph_neb(edges, vtxs)
        graph = get_graph_neb(edges, vtxs)
        for vtx in vtxs:
            vtx_id = vtx[0]
            vtx_label = vtx[1]
            neb_nodes = neb_dict[vtx_id]
            node_L = label_codes[vtx_label]
            node_N = get_abj_coding(neb_nodes, label_codes, vtxs_label)
            node_Eigenvalues = get_node_Eigenvalues(vtx_id, graph, 1)
            vtxs_coding.append([vtx[0], node_L, node_N, node_Eigenvalues[0:2]])
        graph_vtxs_coding[key] = vtxs_coding

    id, vtx_nub = find_max_vtxs(dataVtx)

    paser_DT(id, vtx_nub,graph_vtxs_coding)

    pass


if __name__ == '__main__':
    main()
