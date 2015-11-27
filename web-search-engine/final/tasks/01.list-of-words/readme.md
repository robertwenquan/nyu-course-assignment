## List of words

#### Objective

Get a list of 25 common objects for research purpose

#### Method

Based on the MSCOCO (Microsoft Common Object) 2014 training dataset, count the object frequency and get the top 50 object names.
Then hand filter the top25.

#### Use of the data

With the list of common object, like ['cup', 'cat', 'dog', 'meat'], we will crawl the corresponding images for them respectively with various approaches: 
1. common text crawl
 1.1 google
 1.2 bing
2. image crawl
 2.1 google
 2.2 bing
3. stock photo crawl
 3.1 shutterstock
 3.2 ???
4. social media crawl
 4.1 flickr
 4.2 tumblr
 
Then we will measure the accuracy of each crawl for each object.

#### Research
The object annotations are recoreded in instances_train2014.json 
It is packed in http://msvocds.blob.core.windows.net/annotations-1-0-3/instances_train-val2014.zip

There are 604k labeled objects in this MSCOCO 2014 Training dataset. 

```
$ jq .annotations[].category_id annotations/instances_train2014.json | wc -l
604907

Here are the objects with top and bottom frequencies. The top one is 'person' with more than 185k occurrences. The bottom one is 'hair drier' with only 135 occurrences.

$ jq .annotations[].category_id annotations/instances_train2014.json | sort | uniq -c | sort -k1nr | head -n25
 185316  1 person
  30785  3 car
  27147 62 chair
  17315 84 book
  16983 44 bottle
  14513 47 cup
  11167 67 dining table
  10064 51 bowl
   9159 10 traffic light
   8778 31 handbag
   7865 28 umbrella
   7590  9 boat
   7290 16 bird
   7050  8 truck
   6912 52 banana
   6751 15 bench
   6654 20 sheep
   6560 38 kite
   6200 27 backpack
   6021  4 motorcycle
   5918 64 potted plant
   5686 21 cow
   5618 46 wine glass
   5539 57 carrot
   5536 49 knife

$ jq .annotations[].category_id annotations/instances_train2014.json | sort | uniq -c | sort -k1nr | tail -n20
   2905 65 bed
   2873 70 toilet
   2689 40 baseball glove
   2400 39 baseball bat
   2302 79 oven
   2023 58 hot dog
   1980 76 keyboard
   1960 36 snowboard
   1875 82 refrigerator
   1862 34 frisbee
   1517 74 mouse
   1377 90 toothbrush
   1372 13 stop sign
   1316 11 fire hydrant
   1189 78 microwave
   1073 87 scissors
    903 23 bear
    833 14 parking meter
    156 80 toaster
    135 89 hair drier

Then with manual filtering, we get the below list of 25 object names for research: 

["car", "chair", "bottle", "umbrella", "boat", "bird", "truck", "bench", "sheep", "banana", "kite", "motorcycle", "cow", "carrot", "knife", "bed", "hot dog", "keyboard", "refrigerator", "frisbee", "toothbrush", "fire hydrant", "scissors", "bear", "hair drier"]

```

#### Deliverable

A list of words: 
-----
car
chair
bottle
umbrella
boat
bird
truck
bench
sheep
banana
kite
motorcycle
cow
carrot
knife
bed
hot dog
keyboard
refrigerator
frisbee
toothbrush
fire hydrant
scissors
bear
hair drier
-----

