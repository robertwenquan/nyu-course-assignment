#!/usr/bin/R -f
#
# R script to calculate cosine distance 
#
# Objective: To calculate the friend relationship distance using Cosine Distance
#
# Input : 'qw476-ranking-data.txt'
#         it is a CSV format file that contains the X and Y values for a list of names
#
# Output: STDOUT
#

# We use dplyr package to filter and clean the data
library(dplyr)

# Load the CSV data(qw476-ranking-data.txt) into a data frame
data <- read.csv('qw476-ranking-data.txt', header = FALSE, col.names = c('Friend', 'x', 'y'))

# Verify the loaded data
str(data)
head(data)
tail(data)

# JOIN the data frame
merge(data, data, by = NULL) %>%

# Remove the lines with same Known and Unknown friend name
filter(Friend.x != Friend.y) %>%

# Change column names to a more user-friendly and recognizable ones
select(Known = Friend.x, Unknown = Friend.y, x1 = x.x, y1 = y.x, x2 = x.y, y2 = y.y) %>%

# Calculate cosine distance and add a column for it
mutate(cosine = round((x1*x2 + y1*y2)/(sqrt(x1^2 * y1^2)*sqrt(x2^2 * y2^2)),2)) %>%

# Sort by Known friend name and display the data frame
arrange(Known)

