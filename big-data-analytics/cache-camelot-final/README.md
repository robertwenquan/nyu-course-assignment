## Big Data Analytics Final Project

### TODO
* A graph about the caching architecture, which part is the game, which part is the caching, which part is the data generation
* Data generation flow chart, including data prepare, filtering, map, reduce, database loading
* Query service flow, for web UI, and game UI

### Introduction

Mini Camelot is a simplified version of a board game Camelot. It has white and black players on each side of the game canvass. Each player has to follow specific moving rules to move their own pieces. In order to maximize the game success rate, artificial intelligence algorism is used in evaluating the optimal moving strategy. However, the calculating time, a.k.a thinking time of the robot player, takes seconds with moderate evaluation level. In this project I am trying to eliminate the thinking time for this Mini Camelot game to an unnoticable level, by pre-calculating the gaming results on Amazon EMR (Elastic Map Reduce) service and store them on local MongoDB for fast cached result query. The design of the data format transformation, as well as how the map-reduce is implemented are elaborated. To evaluate the impact of this proposed idea, a benchmark is designed to compare the performance with and without the cache. Lastly the further opportunites of this idea is discussed. For more details about the camelot game, you can refer to http://en.wikipedia.org/wiki/Camelot_(board_game) or http://www.iggamecenter.com/info/en/camelot.html

### Game Cache Layer Design

##### Cache Layer Introduction

The original mini Camelot game does not have game result cache layer. It calculates the game moving strategy based on the current game canvass on the fly. Here I design the game cache layer as a transparent cache service to the game engine. As the cache needs external database queries, the game is not designed to be fully dependent on the cache layer. If the cache query is not successful, the game will calculate the result on-the-fly. This ensures the availability of the game while maximize the usage of the cache. The other reason to keep the calculating power of the game but not fully depends on the game cache is that the combinations of the game canvass is incredibly high. To the current capacity of the cache design it is not pratical to pre-calculate and store all the cache results of the game. Hence we have to keep the computing power of the game when the cache layer is unaccessible or the cache result is unavailable. When there is a on-the-fly game result is calculated, the new cache entry will be saved into the database for futher query as the optimal move strategy is consistent with a specific game canvass.

##### Cache Storage

The cached results are stored in the document based NoSQL database MongoDB. MongoDB is chosen because of the following reasons. First it is because it suppports native JSON document storage. This eases the data parsing and storage a lot. Without this, data parsing and table design would be very tedious if I want to store the same amount of data into a relational database. Secondly MongoDB has better horizontal scaling than the relational databases. Although in this project we do not have huge amount of data to scale to multiple MongoDB nodes, it is better to consider the growing capacity ahead of time from the architecture point of view. Otherwise there will be disaster when the scaling wall is hit. The third reason to choose MongoDB is because this is the only NoSQL database we covered in this semester. In my personal view it is better to cover this database in this term project.

##### Cache Calculation

The game cached results come from two parts: 

1. Pre-calculated results

  This serves the major portion of the game cached results. 

  This part of the cache is calculated from the prepared list of canvass maps. The calculation is produced outside of the game that the human plays. Instead the game engine is extracted from the main game code and is converted into a map-reduce program to adapt the huge amount of data for calculation. Without the map-reduce, for 1 million game canvass with average 1 second thinking time, we need approximately 11 days on one machine to finish the calculation. With 6 million results we need about two months to finish all the calculation, which is not quite bearable for this project. With the introduction of map-reduce, we could parallel the calculation on multiple nodes and expedite the resutl generation in a much less turnaround time.

1. On-the-fly results

  At the beginning of the cache generation phase, this serves as data collection source for filtering model training. With real human play on the game, a few to plenty real game canvass scenarios could be saved together with the on-the-fly calculated results. 

  After the massive pre-calculated caches are loaded. It will be rare to have the chance to run the on-the-fly result but things will still happen. This serves as the complementary portion of the game cached results when cache miss happens.

### Data Transformation

In order to get the final result, we need some data transformation from the raw data to the final data for consumption. This consists of the following few phases:

  * Data Generation
  * Data Filtering
  * Data Calculation

##### Data generation

  Before the cached results are loaded. We need a list of canvass maps to calculate. Conceptually, there are about 10^18 magnitude of game canvass combinations. Considering an average 1 second thinking time for the on-the-fly calculation, we need 1,000,000 machines to calculate 31,000 years to get the full results. This is obviously not practical at all from the time and resource point of view. Also from the storage point of view, considing an average of 100 bytes per cached result, we need approximately 100 EB to store the cached results, which is also impractical at all.

##### Raw Data Format

Raw data is one or more text files.
Each line is a 25 bytes string, with '\n' excluded, like the following
```
'424344455354X727475767782'
 |            |
 |            727475767782 (black player piece list)
 424344455354 (white player piece list)
```
Each two bytes represents the coordinates of one piece on one side. The first byte represents the row index ranging from 0 to D. The second byte represents the column index ranging from 0 to 7.

It's a 12bytes + 12bytes string with an 'X' in the middle

##### Data Calculation

Data Calculation is the major part of preparation the core data for this project. It runs the stripped core game algorithm to calculate the optimal move stratety

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
conceptually there are approx 10^18 possible game canvass scenarios. Given 

### Result Calculation
 
For each data entry as one combination of the game canvass map, we have 6 scenarios to consider:
1. Difficulty level 1, as white player
1. Difficulty level 1, as black player
1. Difficulty level 2, as white player
1. Difficulty level 2, as black player
1. Difficulty level 3, as white player
1. Difficulty level 3, as black player

In this map-reduce, we have defined two steps.
The first step is to read the mapkey from the raw input, and yield six items for the input of the mapper in the next step.
The second step calculates the game result in the mapper for specified level and side, and combine the results of same mapkey with different levels and sides into one item in the reducer.
For one raw input, there will be six output in phase one.  But in step two after the reducer, the final output will be reduced to only one again.
The two steps are defined as follows:
```python
def steps(self):
  return [MRStep(mapper=self.mapper1),
          MRStep(mapper=self.mapper2, reducer=self.reducer)]
```
Here is the mapper function for step1:
```python
def mapper1(self, _, mapkey):
  '''
  This is the mapper function in step1
  It is to filter the low probability canvass scenarios
  '''
  if self.filter(mapkey) == True:
    yield (None, (mapkey, 1, 'north'))
    yield (None, (mapkey, 1, 'south'))
    yield (None, (mapkey, 2, 'north'))
    yield (None, (mapkey, 2, 'south'))
    yield (None, (mapkey, 3, 'north'))
    yield (None, (mapkey, 3, 'south'))
```
Here is the mapper and reducer function for step2:
```python
def mapper2(self, _, request):
  '''
  This is the mapper function in step2
  It is to transform the canvass map hashkey to real canvass
  and calculate the optimal next move as well as the move statistics

  The result in this step is the final result of this MapReduce job
  '''

  mapkey, level, side = request

  if self.validate_mapkey(mapkey) == False or \
      level < 1 or level > 3 or \
      side != 'north' and side != 'south':
    return

  optimal_path = self.get_game_result(mapkey, level, side)
  yield (mapkey, (level, side, optimal_path))

def reducer(self, key, results):
  '''
  This is the reducer function in step2
  It is to combine the results for all levels and sides into a single dictionary
  and return as a JSON string
  '''

  entry = dict()
  entry[key] = dict()
  entry[key][1] = { 'north' : {}, 'south' : {} }
  entry[key][2] = { 'north' : {}, 'south' : {} }
  entry[key][3] = { 'north' : {}, 'south' : {} }

  for result in results:
    level, side, path = result
    entry[key][level][side] = path

  yield key, entry
```

### Data Importing

### Data Retrieving

### Data Viewing

### Game Benchmark

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

From the result of the benchmark we can see...

##### Technology summary

* Data preparation part is implemented in Python
* Machine learning part is not fully implemented. 
* Big Data part is implemented in Python with MRJob library and it is run on Amazon EMR cloud service
* Query part is implemented in Python with Django web framework
* Visualization part is maily implemented with R but is also combined with Python for GIF animation generation

### Opportunities

The ultimate goal for this game cache layer is to achieve 100% cache hit rate, with acceptable user response time. 

In order to achieve this, we have discussed the impossibility to cover all the game canvass scenarios with reasonable resource in the current technology trend. Dispite of this, increasing the number of cache entries would still increase the probability of cache hit. From this approach, we need to increase the number of computing nodes when doing the pre-calculation map-reduce on Amazone EMR. In the 1 million data sample in this projects, we spent about 58 hours on 16 nodes. Preferrably we would like to run 64-128 nodes so we can reduce the elapsed time to less than 10 hours for the 1 million data items.

Now that we cannot cover all the game canvass scenarios, we will need to optimize our filtering model to keep the most effective game canvass in the cache. As this is a trained model, we will need more training data. With the single machine mini camelot game, it is difficult to collect a good amount of training data with only one human game player. Also with limited human player, it is difficult to get training data with variety in terms of moving habits and strategies. If the game could be extended to an online version, with more human players, it will be much easier to collect a lot of good training samples in a short period of time. Then with sufficient real game play data, we could train a better filtering model to increase the cache hit rate.

### References
* MRjob
* MongoDB

