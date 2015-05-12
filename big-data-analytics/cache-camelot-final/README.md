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
'404142434445X121314152122'
```
It's a 12bytes + 12bytes string with an 'X' in the middle

##### Final Data Format

```
"404142434445X121314152132"     [[[4, 0], [3, 0]], [2, 155, 0, 40]]
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

