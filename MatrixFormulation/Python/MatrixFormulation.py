import numpy as np
import networkx as nx
import csv
import sys

file="../Graph/directedEdges.csv"

beta=0.9

# create networkx graph
G=nx.DiGraph()

#Open File and read directed Edges from each line
with open(file) as f:
    reader = csv.reader(f)
    for row in reader:
       G.add_edge(row[0], row[1])

graphNodes = G.nodes()
importanceContributionDictionary = {}

for gnode in graphNodes:
   #calculate outdegree for each node
   nodeOutDegree = G.out_degree(gnode)
   #if outdegree is 0, importance contribution is 0 else 1/outdegree
   if nodeOutDegree == 0 :
      importanceContributionDictionary[gnode] = 0.0
   else:
      importanceContributionDictionary[gnode] = 1.0/nodeOutDegree

#length of graphNodes
graphNodesLength = len(graphNodes)

#Initialize stochastic matrix with zeroes
stochasticMatrix = np.zeros((graphNodesLength,graphNodesLength))

i = 0
#replace zeroes with coefficients in stochasticMatrix
for gnode in graphNodes:
   nodeInnerEdges = G.in_edges(gnode)
   for inLinkEdgeNode in [linkEdge[0] for linkEdge in nodeInnerEdges]:
      stochasticMatrix[i,graphNodes.index(inLinkEdgeNode)] = 1.0*importanceContributionDictionary[inLinkEdgeNode]
   i = i + 1

#add (1-beta)/numberOfNodes*matrixwithallones for spidertraps, deadends and self-loops
stochasticMatrix = beta*stochasticMatrix + (1-beta)/graphNodesLength*np.ones((graphNodesLength,graphNodesLength))

#initialize random page ranks for each node
pageRanks = np.random.random_sample((graphNodesLength,))

#sum of pageranks must be one
pageRanks = pageRanks/pageRanks.sum()


#Iterative Calculation for Pageranks
for i in range(0, 1000):
     tempPageRanks = np.dot(stochasticMatrix,pageRanks)
     tempPageRanks = tempPageRanks/tempPageRanks.sum()
     if np.absolute(pageRanks - tempPageRanks).sum() < 0.000001:
        pageRanks = tempPageRanks
        break
     else:
        pageRanks = tempPageRanks

#zip with graphNodes to know pageRanks of each corresponding node
dictionary = dict(zip(graphNodes, pageRanks))

#print node and its page rank
print dictionary



