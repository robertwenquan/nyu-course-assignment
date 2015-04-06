#!/usr/bin/R -f

#
# R script to calculate manhatten distance 
#

library(dplyr)

data <- read.csv('qw476-ranking-data.txt', header = FALSE, col.names = c('Friend', 'x', 'y'))

merge(data, data, by = NULL) %>%
filter(Friend.x != Friend.y) %>%
select(Known = Friend.x, Unknown = Friend.y, x1 = x.x, y1 = y.x, x2 = x.y, y2 = y.y) %>%
mutate(manhatten = abs(x1-y2) + abs(y1-y2)) %>%
arrange(Known)

