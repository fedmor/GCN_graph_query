f = open('./s1_dome.txt')
v = open('./s1_vtx.txt', 'w')
e = open('./s1_edge.txt', 'w')

count = 0
while True:
    line = f.readline().strip('\n')
    if not line: break
    if "*" in line: continue
    nodes = line.split(" ")
    if nodes[0] is "v":
        v.writelines(nodes[1]+" "+nodes[2]+"\n")
    elif nodes[0] is "e":
        e.writelines(nodes[1]+" "+nodes[2]+" "+nodes[3]+"\n")
f.close()
v.close()
e.close()