import sys
import math
import operator
import networkx as nx
from sklearn import datasets
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn import cross_validation

#jaccard
def Jaccard(node1, node2):
    node1Neighbor = G.neighbors(node1)
    node2Neighbor = G.neighbors(node2)
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


# G = nx.Graph()

# f = open( 'train_edges.txt', 'r' )
# f.readline()
# f.readline() #skip first two lines
# while True:
#     line = f.readline()
#     if len(line) == 0:
#         break
#     nodes = [int(s) for s in line.split() if s.isdigit()]
#     G.add_edge(nodes[0], nodes[1])
# f.close()
# print('create graph complete')

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

# with open('svm_train.txt', 'w') as f:
#     for node in G.nodes():
#         for neighbor in G.neighbors(node):
#             print(node, neighbor)
#             print(1, end=' ', file=f)
#             features = naive_profile_features(node, neighbor)
#             for i in range(0, len(features)):
#                 print(i+1, features[i], sep=':', end=' ', file=f)
#             print('', file=f)

(trainX, trainY) = datasets.load_svmlight_file("svm_train.txt")
classifier = svm.OneClassSVM()
classifier.fit(trainX)
scores = cross_validation.cross_val_score(classifier, trainX, trainY, cv = 5, scoring = "f1")
print(scores)