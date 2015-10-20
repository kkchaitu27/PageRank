require(igraph)

directedEdges <- read.csv("../Graph/directedEdges.csv", header=FALSE)

directedEdges.network<-graph.data.frame(directedEdges, directed=T)

plot(directedEdges.network)

V(directedEdges.network)$name
E(directedEdges.network)[from(V(directedEdges.network)[1])]
adjacent_vertices(directedEdges.network, '1')

from(V(directedEdges.network)[1])
     