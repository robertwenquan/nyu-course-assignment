## Big Data Analytics Final Project

### Introduction

What problem we are trying to solve?
What benefit will we have?
We have an 
In order to expedite the thinking time of the robot, a smart caching layer is introduced for this game

##### Introducion about the Mini Camelot Game

Here is a few reference links for the Camelot game:
* http://en.wikipedia.org/wiki/Camelot_(board_game)
* http://www.iggamecenter.com/info/en/camelot.html

### Data Transformation

In order to get the final result, we need some data transformation from the raw data format to the final data format.

##### Raw Data Format

Raw data is one or more text files.
Each line is a 25 bytes string, with '\n' excluded, like the following
```
'424344455354X727475767782'
```
It's a 12bytes + 12bytes string with an 'X' in the middle

##### Final Data Format

```
{u'424344455354X727475767782': {u'1': 
                                 {u'north': [[[4, 3], [6, 3], [8, 1], [8, 3], [6, 5], [8, 5], [6, 7], [8, 7]],
                                             [1, 23, 0, 0],
                                             [u'424344455354X727475767782', u'424445535463X727475767782', 
                                              u'424445535481X747576778200', u'424445535483X747576770000', 
                                              u'424445535465X757677000000', u'424445535485X767700000000',
                                              u'424445535467X770000000000', u'424445535487X000000000000'],
                                             0.006062984466552734],
                                  u'south': [[[8, 2], [6, 2]],
                                             [1, 44, 0, 0],
                                             [u'424344455354X727475767782', u'424344455354X627274757677'],
                                             0.017976999282836914]},
                                u'2': 
                                 {u'north': [[[4, 3], [6, 3], [8, 1], [8, 3], [6, 5], [8, 5], [6, 7], [8, 7]],
                                             [1, 23, 0, 0],
                                             [u'424344455354X727475767782', u'424445535463X727475767782', 
                                              u'424445535481X747576778200', u'424445535483X747576770000', 
                                              u'424445535465X757677000000', u'424445535485X767700000000',
                                              u'424445535467X770000000000', u'424445535487X000000000000'],
                                             0.0057909488677978516],
                                  u'south': [[[7, 4], [8, 5]],
                                             [2, 1202, 0, 39],
                                             [u'424344455354X727475767782', u'424344455354X727576778285'],
                                             0.45843982696533203]},
                                u'3': 
                                 {u'north': [[[4, 3], [6, 3], [8, 1], [8, 3], [6, 5], [8, 5], [6, 7], [8, 7]],
                                             [1, 23, 0, 0],
                                             [u'424344455354X727475767782', u'424445535463X727475767782', 
                                              u'424445535481X747576778200', u'424445535483X747576770000', 
                                              u'424445535465X757677000000', u'424445535485X767700000000',
                                              u'424445535467X770000000000', u'424445535487X000000000000'],
                                             0.006079196929931641],
                                  u'south': [[[7, 4], [8, 5]],
                                             [3, 20786, 1142, 37],
                                             [u'424344455354X727475767782', u'424344455354X727576778285'],
                                             6.91152811050415]}}}``
```

##### Data Filtering

Although there are only 6 pieces for white and black side respectively, on a 88-cell game canvass, 
conceptually there are approx 10^19 possible game canvass scenarios. Given 

### Result Calculation
 
For each data entry as one combination of the game canvass map, we have 6 scenarios to consider:
1. Difficulty level 1, as white player
2. Difficulty level 2, as white player
3. Difficulty level 3, as white player
4. Difficulty level 1, as black player
5. Difficulty level 2, as black player
6. Difficulty level 3, as black player

### Benchmark

* Workload
** The combination of workload scenarios we use for the benchmark
** In order to make the workload typical, we recorded the game canvass map evolution with a real play.
** There are totoally XXX moves in this game. Among those there are XXX moves for the robot player.
* Without the smart cache
** How many seconds we need to run the benchmark
** Move1 (A->B), xxx seconds
** Move2 (A->B), xxx seconds
** Move3 (A->B), xxx seconds
** Move4 (A->B), xxx seconds
** Aggregated, xxxxx seconds
* With the smart cache
** How many seconds we need to run the benchmark
** Move1 (A->B), xxx seconds
** Move2 (A->B), xxx seconds
** Move3 (A->B), xxx seconds
** Move4 (A->B), xxx seconds
** Aggregated, xxxxx seconds
* Compare the time spent in two modes in a chart

### Summary
* What have we achieved?

### TODO?
* Bigger data?
** Bigger data will increase the cache hit rate
* Less data?
** With training data from the real plays, we will have a better model to classify the game canvass

### References
* MRjob
* MongoDB

