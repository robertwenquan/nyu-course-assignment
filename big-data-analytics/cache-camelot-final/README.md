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

### Benchmark

* Workload
** The combination of workload scenarios we use for the benchmark
* Without the smart cache
** How many seconds we need to run the benchmark
* With the smart cache
** How many seconds we need to run the benchmark

### Summary
* What have we achieved?

### TODO?
* Bigger data?

### References

