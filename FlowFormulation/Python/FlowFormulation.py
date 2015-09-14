import numpy as np
import networkx as nx
import csv
import sys

####################################################################################################################
# Example Code for hard-coded values given below
#if graph = [(1, 2), (1, 3), (1,4), (2, 3), (3, 4), (3,5), (4, 5), (5, 2),(5,1)]
#Equations are,
#x1=x5/2
#x2=x1/3+x5/2
#x3=x2+x1/3
#x4=x3/2+x1/3
#x5=x3/2+x4
#X = np.array([[1,0,0,0,-1.0/2],[-1.0/3,1,0,0,-0.5],[-1.0/3,-1,1,0,0],[-1.0/3,0,-0.5,1,0],[0.0,0,-0.5,-1,1],[1,1,1,1,1]])

#Y = np.array([0,0,0,0,0,1])

#A = np.column_stack((X,np.ones(X.shape[0])))

#print A

#print np.linalg.lstsq(A, Y)[0]
####################################################################################################################


#In this Flow Formulation, Self Loops,Spider Traps and Dead Ends in Graph are not supported

file="../Graph/directedEdges.csv"

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
   nodeOutDegree = G.out_degree(gnode)
   if nodeOutDegree == 0 :
      importanceContributionDictionary[gnode] = 0.0
   else:
      importanceContributionDictionary[gnode] = 1.0/nodeOutDegree

graphNodesLength = len(graphNodes)
equationMatrix = np.zeros((graphNodesLength,graphNodesLength))

i = 0
for gnode in graphNodes:
   equationMatrix[i,i] = 1.0
   nodeInnerEdges = G.in_edges(gnode)
   if len(nodeInnerEdges) == 0:
      sys.exit("This cannot handle Dead Ends!!!")
   for inLinkEdgeNode in [linkEdge[0] for linkEdge in nodeInnerEdges]:
      equationMatrix[i,graphNodes.index(inLinkEdgeNode)] = -1.0*importanceContributionDictionary[inLinkEdgeNode]
   i = i+1

finalCoefficientMatrix = np.vstack([equationMatrix,np.ones(graphNodesLength)])

Y = np.hstack([np.zeros(graphNodesLength),[1.0]])

xWithBias = np.column_stack((finalCoefficientMatrix,np.ones(finalCoefficientMatrix.shape[0])))

dictionary = dict(zip(graphNodes, np.linalg.lstsq(xWithBias, Y)[0]))

print dictionary

