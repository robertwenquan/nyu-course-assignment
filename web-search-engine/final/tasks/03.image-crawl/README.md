### crawled images from various image sources

* image search engine: google image
* social media: tumblr, flickr
* stock photo

```
$ jq --raw-output .query crawl-wse_google_image.log | sort | uniq -c | sort -k1 -rn
 893 bottle
 888 kite
 880 bear
 865 carrot
 841 banana
 835 frisbee
 820 sheep
 810 hot dog
 809 toothbrush
 795 scissors
 774 fire hydrant
 711 hair drier
 677 boat
 676 motorcycle
 662 bench
 628 keyboard
 624 car
 613 truck
 575 cow
 542 refrigerator
 533 knife
 525 bird
 500 umbrella
 474 chair
 417 bed
```

```
$ jq --raw-output .query crawl-wse_tumblr.log | sort | uniq -c | sort -k1 -rn
1009 fire hydrant
1008 kite
1007 chair
1007 bottle
1007 bench
1007 bed
1006 carrot
1006 bear
1005 scissors
1005 car
1005 boat
1004 truck
1004 toothbrush
1004 sheep
1004 refrigerator
1004 motorcycle
1004 knife
1004 banana
1003 bird
1002 hot dog
1001 keyboard
1001 frisbee
 258 umbrella
 216 cow
  61 hair drier
```

```
$ jq --raw-output .query crawl-wse_flickr.log | sort | uniq -c | sort -k1 -rn
 701 toothbrush
 701 kite
 701 keyboard
 701 hot dog
 701 frisbee
 701 fire hydrant
 701 bench
 700 scissors
 700 bear
 699 hair drier
 699 carrot
 699 banana
 698 truck
 698 knife
 696 cow
 695 boat
 695 bed
 694 motorcycle
 693 bird
 692 bottle
 689 sheep
 686 chair
 680 refrigerator
 603 umbrella
 601 car
```

