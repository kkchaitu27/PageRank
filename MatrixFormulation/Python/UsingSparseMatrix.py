import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

webGoogle = pd.read_csv('/home/krishna/Projects/PageRank/MatrixFormulation/Graph/web-Google.txt', sep='\t', comment='#', names=['from', 'to'])

beta = 0.8

data = np.repeat(1, webGoogle.shape[0])
categories = np.unique(webGoogle.values)
categories.sort()

noOfNodes = len(categories)

codes = np.arange(0,noOfNodes)

replacementCodes = pd.DataFrame({"node" : categories, "code" : codes})

replaceDict = dict(zip(categories,codes))

fromReplaced = pd.merge(webGoogle,replacementCodes,left_on="from",right_on="node")

fromReplaced.columns = ["from","to","fromReplacement","node"]

toFromReplaced = pd.merge(fromReplaced[["from","to","fromReplacement"]],replacementCodes,left_on="to",right_on="node")

toFromReplaced.columns = ["from","to","fromReplacement","toReplacement","node"]

row_ind = toFromReplaced['fromReplacement']
col_ind = toFromReplaced['toReplacement']

freq = np.bincount(row_ind)
nodes = np.nonzero(freq)[0]
freqWithNodes = pd.DataFrame({"node" : nodes,"frequency" : freq[nodes]})

preprocessedData = pd.merge(toFromReplaced,freqWithNodes,left_on="fromReplacement",right_on="node")


M = csr_matrix((1.0/preprocessedData['frequency'], (preprocessedData["fromReplacement"], preprocessedData["toReplacement"]))).transpose()

print M.shape

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

print pageRanks[replaceDict.get(99)]



