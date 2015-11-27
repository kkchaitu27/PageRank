#Fast loading of Data
require(data.table)

#for dealing with Sparse Matrices
require(Matrix)

#probability for visiting a link through edge
beta = 0.8

#load directed edges from the file
rawdata <- fread("../Graph/web-Google.txt",col.names=c("from","to"))

#Number of unique Nodes in the data
nodes <- sort(unique(c(rawdata$from,rawdata$to)))

#Replacing unique nodes with numbers
nodeNumbers <- c(1:length(nodes))
nodeLookup <- data.frame(nodes,nodeNumbers)

#Merging nodeLookup to find replacement of from nodes
fromNodesWithReplacement <- merge(rawdata,nodeLookup,by.x="from",by.y="nodes")

#column names of merged rawdata with from nodes
colnames(fromNodesWithReplacement) <- c("from","to","fromReplacement")

#Merging fromNodesWithReplacement to find replacement of to nodes
allNodesWithReplacement <- merge(fromNodesWithReplacement,nodeLookup,by.x="to",by.y="nodes")

#column names of above merged data with to nodes
colnames(allNodesWithReplacement) <- c("to","from","fromReplacement","toReplacement")

#Calculating number of outlinks for each node
freqOfEachNode <- as.data.frame(table(allNodesWithReplacement$fromReplacement))
freqOfEachNode$Var1 <- as.numeric(as.character(freqOfEachNode$Var1))
reqData <- subset(allNodesWithReplacement, select=c("fromReplacement", "toReplacement"))
matrixWithFreq <- merge(reqData,freqOfEachNode,by.x="fromReplacement",by.y="Var1")

#sparse Matrix representation
webGraph <- t(sparseMatrix(i = matrixWithFreq$fromReplacement,j = matrixWithFreq$toReplacement,x=1.0/matrixWithFreq$Freq))

#Number of nodes in this graph
noOfVertices <- nrow(webGraph)

#initializing page ranks with 1/noOfVetices
pageRanks <- rep(1/noOfVertices,noOfVertices)

#Iterative Calculation for Pageranks
for (i in 1:1000){
  tempPageRanks <- beta*as.numeric((webGraph %*% pageRanks)) + (1-beta)/noOfVertices
  rankSum = sum(tempPageRanks)
  tempPageRanks = tempPageRanks + (1-rankSum)/noOfVertices
  comparisonValue <- sum(abs(pageRanks - tempPageRanks))
  if(comparisonValue < 0.000001){
    pageRanks = tempPageRanks
    break
  }else{
    pageRanks = tempPageRanks
  }
}

#Finding replacement value for node 99
Node99Replacement = allNodesWithReplacement[allNodesWithReplacement$from==99]$fromReplacement[1]
#Printing page rank of Node 99
print(pageRanks[Node99Replacement])


