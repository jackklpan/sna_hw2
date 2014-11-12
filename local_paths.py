from __future__ import print_function
import sys
import math
import operator
import random
import networkx as nx
from sklearn import datasets
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn import cross_validation

#jaccard
def Jaccard(node1, node2):
    node1Neighbor = G.neighbors(node1)
    node2Neighbor = G.neighbors(node2)
    if len(set(node1Neighbor) | set(node2Neighbor)) == 0:
        return 0
    else:
        return len(set(node1Neighbor) & set(node2Neighbor)) / len(set(node1Neighbor) | set(node2Neighbor))

def Shortest_Path(node1, node2, graph):
    return 1/len(nx.shortest_path(graph, source=node1,target=node2))

def naive_profile_features(node1, node2):
    numerical_Type_Column = [45, 6, 16, 49]
    features = []
    for i in range(1, 55):
        if i not in numerical_Type_Column:
            features.append( len( set(G.node[node1][i]) & set(G.node[node2][i]) ) )
        else:
            if len(G.node[node1][i])>0 and len(G.node[node2][i])>0:
                features.append( abs( G.node[node1][i][0] - G.node[node2][i][0] ) )
            else:
                features.append( 0 )
    return features


G = nx.Graph()
GForScipy = nx.Graph()
maxNodeId = 0

f = open( 'train_edges.txt', 'r' )
f.readline()
f.readline() #skip first two lines
while True:
    line = f.readline()
    if len(line) == 0:
        break
    nodes = [int(s) for s in line.split() if s.isdigit()]
    G.add_edge(nodes[0], nodes[1])
    GForScipy.add_edge(nodes[0], nodes[1])
    if nodes[0] > maxNodeId:
        maxNodeId = nodes[0]
    if nodes[1] > maxNodeId:
        maxNodeId = nodes[1]
f.close()
print('create graph complete')

for i in range(0, maxNodeId):
    if not GForScipy.has_node(i):
        GForScipy.add_node(i)

ajMatrix = nx.to_scipy_sparse_matrix(GForScipy)
ajMatrix2 = ajMatrix * ajMatrix
ajMatrix3 = ajMatrix2 * ajMatrix
eps = 0.01
# for g in nx.connected_component_subgraphs(G):
#     print(nx.average_shortest_path_length(g))

# f = open( 'pre_nodes_profile.csv', 'r' )
# f.readline()
# while True:
#     line = f.readline()
#     if len(line) == 0:
#         break
#     s = line.split(',')
#     nodeNum = int(s[0])
#     if not G.has_node(nodeNum):
#         G.add_node(nodeNum)

#     for i in range(1, len(s)):
#         G.node[nodeNum][i] = [int(attr) for attr in s[i].split() if attr.isdigit()]
#     #print(nodeNum, G.node[int(s[0])][len(s)-1])
# f.close()
# print('read attributes complete')

scoreSum = 0
minumScore = 1000000
for node in G.nodes():
    for neighbor in G.neighbors(node):
        score = ajMatrix2[node, neighbor] + eps*ajMatrix3[node, neighbor]
        scoreSum = scoreSum + ajMatrix2[node, neighbor] + eps*ajMatrix3[node, neighbor]
        if minumScore > score:
            minumScore = score

# scoreThreshold = (scoreSum / G.number_of_edges()) * 2 * 0.8
#scoreThreshold = minumScore
scoreThreshold = 10.182396203
#16.2918339248 LP
print(scoreThreshold)

deleteEdges = []
for node in G.nodes():
    for neighbor in G.neighbors(node):
        if random.random() >= 0.8:
            deleteEdges.append([node, neighbor])
            G.remove_edge(node, neighbor)

print('start simple test')
correctDetect = 0
for edge in deleteEdges:
    if (ajMatrix2[edge[0], edge[1]] + eps*ajMatrix3[edge[0], edge[1]]) >= scoreThreshold:
        correctDetect = correctDetect + 1
    G.add_edge(edge[0], edge[1])

print(len(deleteEdges))
print(correctDetect / len(deleteEdges))

f = open( 'test_nodes.txt', 'r' )
line = f.readline()
test_nodes = [int(s) for s in line.split() if s.isdigit()]
f.close()
for node in test_nodes:
    if not G.has_node(node):
        G.add_node(node)
with open('output_file2.txt', 'w') as f:
    count = 0
    for node in test_nodes:
        print(node, ":", sep="", end="", file=f)
        passThreshold = {}
        for test_neighbor in G.nodes():
            score = ajMatrix2[node, test_neighbor] + eps*ajMatrix3[node, test_neighbor]
            if score > scoreThreshold and (not G.has_edge(node, test_neighbor)) and node != test_neighbor:
                passThreshold[test_neighbor] = score

        passThreshold_sorted = sorted( passThreshold.items(), key=operator.itemgetter(1), reverse=True)
        if len(passThreshold_sorted) > 30:
            passThreshold_sorted = passThreshold_sorted[0:30]
        passThreshold = [str(x[0]) for x in passThreshold_sorted]
        print(passThreshold)
        print(','.join(passThreshold), file=f)