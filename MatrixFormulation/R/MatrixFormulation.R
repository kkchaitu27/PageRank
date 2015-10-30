#load igraph package for graph analysis
require(igraph)

beta = 0.9
#load directed edges from the file
directedEdges <- read.csv("../Graph/directedEdges.csv", header=FALSE)

#convert above dataframe into graph data frame of igraph
directedEdges.network<-graph.data.frame(directedEdges, directed=T)

#Calculate number of vertices from the graph
noofvertices <- length(V(directedEdges.network)$name)

#initialize stochastic matrix with zeroes
stochasticMatrix <- matrix(0,noofvertices,noofvertices)

#Creating Coefficient matrix from the data
i = 1
for (node in sort(V(directedEdges.network)$name)) {
  for (vertex in V(directedEdges.network)[nei(node,"in")]){
    stochasticMatrix[i,match(vertex,V(directedEdges.network)$name)] = 1.0/as.integer(degree(directedEdges.network,vertex,mode=c("out")))
  }
  i = i+1
}

#add (1-beta)/numberOfNodes*matrixwithallones for spidertraps, deadends and self-loops
stochasticMatrix = beta*stochasticMatrix + (1-beta)/noofvertices*matrix(1,noofvertices,noofvertices)

#initialize random page ranks for each node
pageRanks = rep(1.0/noofvertices,noofvertices)

#sum of pageranks must be one
pageRanks = pageRanks/sum(pageRanks)

#Iterative Calculation for Pageranks
for (i in 1:1000){
#  print(pageRanks)
  tempPageRanks <- stochasticMatrix %*% pageRanks
#  print(tempPageRanks)
  rankSum = sum(tempPageRanks)
  tempPageRanks = tempPageRanks + (1-rankSum)/noofvertices
  if (sum(abs(pageRanks - tempPageRanks)) < 0.000001){
    pageRanks = tempPageRanks
    break
  }else{
   pageRanks = tempPageRanks
  }
}

#Printing Vertices First
print(sort(V(directedEdges.network)$name))
#Printing PageRanks of above vertices
print(pageRanks)
