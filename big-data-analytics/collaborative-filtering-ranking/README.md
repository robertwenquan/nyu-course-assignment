## Distance Analysis using R
#### for Manhatten, Euclidean, Cosine and Pearson distance measurement using R

This is a course assignment for the Big Data Analytics class in Spring 2015 semester<br>
Robert Wen (robert.wen@nyu.edu), N12246277, NetID: qw476<br>

#### Manhatten Distance

```
# ./qw476-manhatten-ranking.r
> #!/usr/bin/R -q -f
> #
> # R script to calculate manhatten distance
> #
> # Objective: To calculate the friend relationship distance using Manhatten Distance
> #
> # Input : 'qw476-ranking-data.txt'
> #         it is a CSV format file that contains the X and Y values for a list of names
> #
> # Output: STDOUT, with an add-on column for the manhatten distance between friends
> #
>
> # We use dplyr package to filter and clean the data
> library(dplyr)

Attaching package: ‘dplyr’

The following object is masked from ‘package:stats’:

    filter

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

>
> # Load the CSV data(qw476-ranking-data.txt) into a data frame
> data <- read.csv('qw476-ranking-data.txt', header = FALSE, col.names = c('Friend', 'x', 'y'))
>
> # Verify the loaded data
> str(data)
'data.frame':   4 obs. of  3 variables:
 $ Friend: Factor w/ 4 levels "James","Linda",..: 1 2 3 4
 $ x     : int  3 3 15 6
 $ y     : int  12 12 15 15
> head(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
> tail(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
>
> # JOIN the data frame
> merge(data, data, by = NULL) %>%
+
+ # Remove the lines with same Known and Unknown friend name
+ filter(Friend.x != Friend.y) %>%
+
+ # Change column names to a more user-friendly and recognizable ones
+ select(Known = Friend.x, Unknown = Friend.y, x1 = x.x, y1 = y.x, x2 = x.y, y2 = y.y) %>%
+
+ # Calculate Manhatten distance and add a column for it
+ mutate(manhatten = abs(x1-x2) + abs(y1-y2)) %>%
+
+ # Sort by Known friend name and display the data frame
+ arrange(Known)
     Known Unknown x1 y1 x2 y2 manhatten
1    James   Linda  3 12  3 12         0
2    James    Rita  3 12 15 15        15
3    James Roberto  3 12  6 15         6
4    Linda   James  3 12  3 12         0
5    Linda    Rita  3 12 15 15        15
6    Linda Roberto  3 12  6 15         6
7     Rita   James 15 15  3 12        15
8     Rita   Linda 15 15  3 12        15
9     Rita Roberto 15 15  6 15         9
10 Roberto   James  6 15  3 12         6
11 Roberto   Linda  6 15  3 12         6
12 Roberto    Rita  6 15 15 15         9
>
>
```

#### Euclidean Distance

```
# ./qw476-euclidean-ranking.r
> #!/usr/bin/R -q -f
> #
> # R script to calculate euclidean distance
> #
> # Objective: To calculate the friend relationship distance using Euclidean Distance
> #
> # Input : 'qw476-ranking-data.txt'
> #         it is a CSV format file that contains the X and Y values for a list of names
> #
> # Output: STDOUT, with an add-on column for the euclidean distance between friends
> #
>
> # We use dplyr package to filter and clean the data
> library(dplyr)

Attaching package: ‘dplyr’

The following object is masked from ‘package:stats’:

    filter

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

>
> # Load the CSV data(qw476-ranking-data.txt) into a data frame
> data <- read.csv('qw476-ranking-data.txt', header = FALSE, col.names = c('Friend', 'x', 'y'))
>
> # Verify the loaded data
> str(data)
'data.frame':   4 obs. of  3 variables:
 $ Friend: Factor w/ 4 levels "James","Linda",..: 1 2 3 4
 $ x     : int  3 3 15 6
 $ y     : int  12 12 15 15
> head(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
> tail(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
>
> # JOIN the data frame
> merge(data, data, by = NULL) %>%
+
+ # Remove the lines with same Known and Unknown friend name
+ filter(Friend.x != Friend.y) %>%
+
+ # Change column names to a more user-friendly and recognizable ones
+ select(Known = Friend.x, Unknown = Friend.y, x1 = x.x, y1 = y.x, x2 = x.y, y2 = y.y) %>%
+
+ # Calculate euclidean distance and add a column for it
+ mutate(euclidean = round(sqrt((x1-x2)^2 + (y1-y2)^2),2)) %>%
+
+ # Sort by Known friend name and display the data frame
+ arrange(Known)
     Known Unknown x1 y1 x2 y2 euclidean
1    James   Linda  3 12  3 12      0.00
2    James    Rita  3 12 15 15     12.37
3    James Roberto  3 12  6 15      4.24
4    Linda   James  3 12  3 12      0.00
5    Linda    Rita  3 12 15 15     12.37
6    Linda Roberto  3 12  6 15      4.24
7     Rita   James 15 15  3 12     12.37
8     Rita   Linda 15 15  3 12     12.37
9     Rita Roberto 15 15  6 15      9.00
10 Roberto   James  6 15  3 12      4.24
11 Roberto   Linda  6 15  3 12      4.24
12 Roberto    Rita  6 15 15 15      9.00
>
>
```

#### Cosine Distance

```
# ./qw476-cosine-ranking.r
> #!/usr/bin/R -q -f
> #
> # R script to calculate cosine distance
> #
> # Objective: To calculate the friend relationship distance using Cosine Distance
> #
> # Input : 'qw476-ranking-data.txt'
> #         it is a CSV format file that contains the X and Y values for a list of names
> #
> # Output: STDOUT, with an add-on column for the cosine distance between friends
> #
>
> # We use dplyr package to filter and clean the data
> library(dplyr)

Attaching package: ‘dplyr’

The following object is masked from ‘package:stats’:

    filter

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

>
> # Load the CSV data(qw476-ranking-data.txt) into a data frame
> data <- read.csv('qw476-ranking-data.txt', header = FALSE, col.names = c('Friend', 'x', 'y'))
>
> # Verify the loaded data
> str(data)
'data.frame':   4 obs. of  3 variables:
 $ Friend: Factor w/ 4 levels "James","Linda",..: 1 2 3 4
 $ x     : int  3 3 15 6
 $ y     : int  12 12 15 15
> head(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
> tail(data)
   Friend  x  y
1   James  3 12
2   Linda  3 12
3    Rita 15 15
4 Roberto  6 15
>
> # JOIN the data frame
> merge(data, data, by = NULL) %>%
+
+ # Remove the lines with same Known and Unknown friend name
+ filter(Friend.x != Friend.y) %>%
+
+ # Change column names to a more user-friendly and recognizable ones
+ select(Known = Friend.x, Unknown = Friend.y, x1 = x.x, y1 = y.x, x2 = x.y, y2 = y.y) %>%
+
+ # Calculate cosine distance and add a column for it
+ mutate(cosine = round((x1*x2 + y1*y2)/(sqrt(x1^2 * y1^2)*sqrt(x2^2 * y2^2)),2)) %>%
+
+ # Sort by Known friend name and display the data frame
+ arrange(Known)
     Known Unknown x1 y1 x2 y2 cosine
1    James   Linda  3 12  3 12   0.12
2    James    Rita  3 12 15 15   0.03
3    James Roberto  3 12  6 15   0.06
4    Linda   James  3 12  3 12   0.12
5    Linda    Rita  3 12 15 15   0.03
6    Linda Roberto  3 12  6 15   0.06
7     Rita   James 15 15  3 12   0.03
8     Rita   Linda 15 15  3 12   0.03
9     Rita Roberto 15 15  6 15   0.02
10 Roberto   James  6 15  3 12   0.06
11 Roberto   Linda  6 15  3 12   0.06
12 Roberto    Rita  6 15 15 15   0.02
>
>
```


#### Pearson Distance

```
# ./qw476-pearson.r
> #!/usr/bin/R -q -f
> #
> # R script to calculate pearson distance
> #
> # Objective: To calculate the pearson distance for a mock-up dataset
> #
> # Input : a mock-up 6-row, 2-column data frame
> #
> # Output: STDOUT, a single value for the pearson distance
> #
>
> # load dplyr package
> library(dplyr)

Attaching package: ‘dplyr’

The following object is masked from ‘package:stats’:

    filter

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

>
> # load the mockup data into a 2 column, 6 row data frame
> data <- data_frame(c(3,4,7,6,8,2),c(5,3,10,8,12,5))
>
> # assign the column names so the data is more readable
> colnames(data) <- c('x', 'y')
>
> # check the data
> data
Source: local data frame [6 x 2]

  x  y
1 3  5
2 4  3
3 7 10
4 6  8
5 8 12
6 2  5
>
> # add STDEV, MEAN, and COUNT into the dataset
> mutate(data, xmean = mean(x), sdx = sd(x), ymean = mean(y), sdy = sd(y), n1 = nrow(data)-1) %>%
+ # add the intermediate value into the dataset
+ mutate(xx = ((x-xmean)/(n1*sdx))*((y-ymean)/(sdy))) %>%
+ # only select the intermediate value column
+ select(xx) %>%
+ # sum it to get the pearson distance
+ sum()
[1] 0.8869758
>
>
```

