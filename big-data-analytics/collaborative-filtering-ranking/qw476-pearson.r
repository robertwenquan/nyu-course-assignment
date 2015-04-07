#!/usr/bin/R -f
#
# R script to calculate pearson distance 
#
# Objective: To calculate the pearson distance for a mock-up dataset
#
# Input : a mock-up 6-row, 2-column data frame
#
# Output: STDOUT, a single value for the pearson distance
#

# load dplyr package
library(dplyr)

# load the mockup data into a 2 column, 6 row data frame
data <- data_frame(c(3,4,7,6,8,2),c(5,3,10,8,12,5))

# assign the column names so the data is more readable
colnames(data) <- c('x', 'y')

# check the data
data

# add STDEV, MEAN, and COUNT into the dataset
mutate(data, xmean = mean(x), sdx = sd(x), ymean = mean(y), sdy = sd(y), n1 = nrow(data)-1) %>%
# add the intermediate value into the dataset
mutate(xx = ((x-xmean)/(n1*sdx))*((y-ymean)/(sdy))) %>%
# only select the intermediate value column
select(xx) %>%
# sum it to get the pearson distance
sum()

