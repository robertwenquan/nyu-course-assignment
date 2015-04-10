#!/usr/bin/R -f

# only square matrices have eigen value/vector
# only positive semi-definite matrices have eigens

# For n X n square matrix, if there are eigen value/vector,
# then there will be n eigen vectors

pcadata <- matrix(c(1,-1,4,2,1,3,1,3,-1),3,3,byrow=T)

pcadata

eigenpcadata <-eigen(pcadata)

eigenpcadata

# eigen value1
evector1 <- eigenpcadata$vectors[,1]
eigenvalue1 <- eigenpcadata$values[1]
evector1
eigenvalue1
eigenvalue1 * evector1

pcadata %*% evector1

# eigen value2
evector2 <- eigenpcadata$vectors[,2]
eigenvalue2 <- eigenpcadata$values[2]
evector2
eigenvalue2
eigenvalue2 * evector2

pcadata %*% evector2


