#importing required packages
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

#Data from Google Page Rank Competition
webGoogle = pd.read_csv('../Graph/web-Google.txt', sep='\t', comment='#', names=['from', 'to'])

#Probability to visit a random link
beta = 0.8

#Link Number for each link in data
data = np.repeat(1, webGoogle.shape[0])
#Number of unique nodes in data
categories = np.unique(webGoogle.values)
#Sorting the categories for numbering them
categories.sort()
#Total Number of nodes in data
noOfNodes = len(categories)
#Code for each node in data
codes = np.arange(0,noOfNodes)
#Pandas Data Frame by replacing nodes with codes
replacementCodes = pd.DataFrame({"node" : categories, "code" : codes})
#Creating dictionary with categories as index and codes as values
replaceDict = dict(zip(categories,codes))
#Replacing FromNodes with Codes
fromReplaced = pd.merge(webGoogle,replacementCodes,left_on="from",right_on="node")
#Renaming for better understanding
fromReplaced.columns = ["from","to","fromReplacement","node"]
#Replacing toNodes with Codes
toFromReplaced = pd.merge(fromReplaced[["from","to","fromReplacement"]],replacementCodes,left_on="to",right_on="node")
#Renaming for better understanding
toFromReplaced.columns = ["from","to","fromReplacement","toReplacement","node"]
#From nodes are taken as rows
row_ind = toFromReplaced['fromReplacement']
#To nodes are taken as columns
col_ind = toFromReplaced['toReplacement']
#Frequency of each node
freq = np.bincount(row_ind)
nodes = np.nonzero(freq)[0]
freqWithNodes = pd.DataFrame({"node" : nodes,"frequency" : freq[nodes]})
#Merging Replaced Nodes with Codes and above frequency for each from node
preprocessedData = pd.merge(toFromReplaced,freqWithNodes,left_on="fromReplacement",right_on="node")

#Sparse Matrix with ToNodes as rows and FromNodes as columns
M = csr_matrix((1.0/preprocessedData['frequency'], (preprocessedData["fromReplacement"], preprocessedData["toReplacement"]))).transpose()

print M.shape
#Initializing pageRank for each Node with 1/noOfNodes
pageRanks = np.repeat(1/noOfNodes, noOfNodes)

#Iterative Calculation for Pageranks
for i in range(1000):
  tempPageRanks = beta*M.dot(pageRanks) + (1-beta)/noOfNodes
  rankSum = sum(tempPageRanks)
  tempPageRanks = tempPageRanks + (1-rankSum)/noOfNodes
  comparisonValue = sum(abs(pageRanks - tempPageRanks))
  if comparisonValue < 0.000001:
    pageRanks = tempPageRanks
    break
  else:
    pageRanks = tempPageRanks

#Page Rank of Specific Node with value 99 in the given dataset
print pageRanks[replaceDict.get(99)]



