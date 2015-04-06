#!/usr/bin/R -f

library(dplyr)

# load the mockup data
data <- data_frame(c(3,4,7,6,8,2),c(5,3,10,8,12,5))

# assign the column names so the data is more readable
colnames(data) <- c('x', 'y')

# check the data
data

# add STDEV, MEAN, and COUNT into the dataset
data2 <- mutate(data, xmean = mean(x), sdx = sd(x), ymean = mean(y), sdy = sd(y), n1 = nrow(data)-1) %>%
mutate(xx = ((x-xmean)/(n1*sdx))*((y-ymean)/(sdy))) %>%
select(xx)

sum(data2)

