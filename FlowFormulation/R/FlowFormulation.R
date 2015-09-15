#load igraph package for graph analysis
require(igraph)

#In this Flow Formulation, Self Loops,Spider Traps and Dead Ends in Graph are not supported

#load directed edges from the file
directedEdges <- read.csv("../Graph/directedEdges.csv", header=FALSE)

#convert above dataframe into graph data frame of igraph
directedEdges.network<-graph.data.frame(directedEdges, directed=T)

#Calculate number of vertices from the graph
noofvertices <- length(V(directedEdges.network)$name)

#Initialize coefficient matrix with zeroes
coefficientMatrix <- matrix(0,noofvertices,noofvertices)

#Creating Coefficient matrix from the data
i = 1
for (node in V(directedEdges.network)$name) {
  coefficientMatrix[i,i] <- 1.0
  for (vertex in V(directedEdges.network)[nei(node,"in")]){
    coefficientMatrix[i,match(vertex,V(directedEdges.network)$name)] = -1.0/as.integer(degree(directedEdges.network,vertex,mode=c("out")))
  }
  i = i+1
}
#Additonal Constraint that all page ranks sum to 1
additionalConstraint = rep(1,noofvertices)
#adding bias
bias = rep(1,noofvertices+1)
#Dependent variable in each equation
Y = c(rep(0,noofvertices),1)

colnames(coefficientMatrix) = V(directedEdges.network)$name
coefficientMatrixWithConstraint = rbind(coefficientMatrix,additionalConstraint)
finalcoefficientMatrix = cbind(coefficientMatrixWithConstraint,bias)

rm(coefficientMatrixWithConstraint,additionalConstraint,bias,i,node,vertex,coefficientMatrix,directedEdges)
#Using linear regression model
model <- lm(Y ~ finalcoefficientMatrix)

#Printing Vertices First
print(V(directedEdges.network)$name)
#Printing PageRanks of above vertices
print(summary(model)$coefficients[c(2:noofvertices+1)])
