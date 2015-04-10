#!/usr/bin/R -f

mx4chol <- matrix(c(2,1,1,3,2,1,2,2,1,1,1,2,9,1,5,3,1,1,7,1,2,1,5,1,8),5,5,byrow=T)
decomposedmx4chol <- chol(mx4chol)

mx4chol
decomposedmx4chol

t(decomposedmx4chol) %*% decomposedmx4chol
