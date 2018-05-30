# -*- coding: utf-8 -*-
from Graph import Graph
from random_simple import simple_sample

#随机获取查询图

def get_sample_query(vtxs_map,path,vtx_mun,graph,start_vtx):

    query_path = simple_sample(graph,start_vtx,0.4,vtx_mun)
    query_vtx = [[vtx,vtxs_map[vtx]] for vtx in query_path]
    query_edges = []
    tmp_path = query_path
    while tmp_path:
        vtx = tmp_path.pop(0)
        children = graph[vtx]
        for i in tmp_path:
            if i in children:
                query_edges.append([vtx,i])
    v_name = path+"vtx_query_"+str(vtx_mun)+".txt"
    e_name = path+"edge_query_"+str(vtx_mun)+".txt"
    w_v = open(v_name, 'w')
    w_e = open(e_name, 'w')
    for item in query_vtx:
        k = str(item[0])+" "+str(item[1])+"\n"
        w_v.writelines(k)
    for item in query_edges:
        k = str(item[0])+" "+str(item[1])+"\n"
        w_e.writelines(k)
    w_v.close()
    w_e.close()


def main():
    vtx_file = open('./data/wordNet/wordnet_vertexes.txt')
    edge_file = open('./data/wordNet/wordnet_edges.txt')
    vtxs_map = {}
    edges = []
    path = './data/wordNet/'

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
    get_sample_query(vtxs_map=vtxs_map,path=path, vtx_mun=10, graph=graph,start_vtx= 60)
if __name__ == '__main__':
    main()