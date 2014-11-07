import sys
import math
import operator
import networkx as nx

#jaccard
def Jaccard(node1, node2):
    node1Neighbor = G.neighbors(node1)
    node2Neighbor = G.neighbors(node2)
    return len(set(node1Neighbor) & set(node2Neighbor)) / len(set(node1Neighbor) | set(node2Neighbor))

def Shortest_Path(node1, node2, graph):
    return 1/len(nx.shortest_path(graph, source=node1,target=node2))

numerical_Type_Column = [45, 6, 16, 49]

G = nx.Graph()

f = open( 'train_edges.txt', 'r' )
f.readline()
f.readline() #skip first two lines
while True:
    line = f.readline()
    if len(line) == 0:
        break
    nodes = [int(s) for s in line.split() if s.isdigit()]
    G.add_edge(nodes[0], nodes[1])
f.close()
print('create graph complete')

f = open( 'pre_nodes_profile.csv', 'r' )
f.readline()
while True:
    line = f.readline()
    if len(line) == 0:
        break
    s = line.split(',')
    print(s)
    for i in range(1, len(s)):
        G.node[int(s[0])][i] = [int(attr) for attr in s[i].split() if attr.isdigit()]
        #print(G.node[int(s[0])][i])
f.close()
print('read attributes complete')

for node in G.nodes():
    for neighbor in G.neighbors(node):
        print(Jaccard(node, neighbor))
        print(Shortest_Path(node, neighbor, G))
		
