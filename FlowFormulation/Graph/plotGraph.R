require(igraph)

directedEdges <- read.csv("../Graph/directedEdges.csv", header=FALSE)

directedEdges.network<-graph.data.frame(directedEdges, directed=T)

plot(directedEdges.network)
