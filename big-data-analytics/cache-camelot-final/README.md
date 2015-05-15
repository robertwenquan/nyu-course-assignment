## Big Data Analytics Final Project

### Introduction

Mini Camelot is a simplified version of a board game Camelot. It has white and black players on each side of the game canvass. Each player has to follow specific moving rules to move their own pieces. In order to maximize the game success rate, artificial intelligence algorism is used in evaluating the optimal moving strategy. However, the calculating time, a.k.a thinking time of the robot player, takes seconds with moderate evaluation level. In this project I am trying to eliminate the thinking time for this Mini Camelot game to an unnoticable level, by pre-calculating the gaming results on Amazon EMR (Elastic Map Reduce) service and store them on local MongoDB for fast cached result query. The design of the data format transformation, as well as how the map-reduce is implemented are elaborated. To evaluate the impact of this proposed idea, a benchmark is designed to compare the performance with and without the cache. Lastly the further opportunites of this idea is discussed. For more details about the camelot game, you can refer to http://en.wikipedia.org/wiki/Camelot_(board_game) or http://www.iggamecenter.com/info/en/camelot.html

### Game Cache Layer Design

##### Cache Layer Introduction

The original mini Camelot game does not have game result cache layer. It calculates the game moving strategy based on the current game canvass on the fly. Here I design the game cache layer as a transparent cache service to the game engine. As the cache needs external database queries, the game is not designed to be fully dependent on the cache layer. If the cache query is not successful, the game will calculate the result on-the-fly. This ensures the availability of the game while maximize the usage of the cache. The other reason to keep the calculating power of the game but not fully depends on the game cache is that the combinations of the game canvass is incredibly high. To the current capacity of the cache design it is not pratical to pre-calculate and store all the cache results of the game. Hence we have to keep the computing power of the game when the cache layer is unaccessible or the cache result is unavailable. When there is a on-the-fly game result is calculated, the new cache entry will be saved into the database for futher query as the optimal move strategy is consistent with a specific game canvass.

##### Cache Calculation

The game cached results come from two parts: 

1. Pre-calculated results

sdfds

1. On-the-fly results

sdfds

##### Cache Storage

The cache 

### Data Transformation

In order to get the final result, we need some data transformation from the raw data format to the final data format.

##### Data generation


##### Raw Data Format

Raw data is one or more text files.
Each line is a 25 bytes string, with '\n' excluded, like the following
```
'424344455354X727475767782'
 |            |
 |            727475767782 (black player piece list)
 424344455354 (white player piece list)

 Each two bytes represents the coordinates of one piece on one side. The first byte represents the row index ranging from 0 to D. The second byte represents the column index ranging from 0 to 7.
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
1. Difficulty level 1, as black player
1. Difficulty level 2, as white player
1. Difficulty level 2, as black player
1. Difficulty level 3, as white player
1. Difficulty level 3, as black player

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

### Opportunities
* Bigger data?
** Bigger data will increase the cache hit rate
* Less data?
** With training data from the real plays, we will have a better model to classify the game canvass

### References
* MRjob
* MongoDB

