### Objectives

Get the predicted labels and image embeddings for the sample images

### How

Run through Clarifai API and get the labeles and extracted high dimensional features

### Deliverables

For each image, the following alike information will be fetched from Clarifai API

The feature embeddings is a 1024 dimensional arrays.
The predicted labels is a varied length of labels with the correponding probabilities.
```
 u'result': {u'embed': [0.0,
                        5.392104148864746,

                        ... (1020 float numbers)

                        0.0,
                        0.698606550693512],

             u'tag': [u'child',
                      u'girl',
                      u'summer',
                      u'outdoors',
                      u'nature',
                      u'people',
                      u'park',
                      u'woman',
                      u'fun',
                      u'leisure',
                      u'flower',
                      u'happiness',
                      u'grass',
                      u'beautiful',
                      u'garden',
                      u'one',
                      u'little',
                      u'leaf',
                      u'smile',
                      u'cute'],

              u'probs': [0.9882996082305908,
                         0.9766360521316528,
                         0.9677201509475708,
                         0.961909830570221,
                         0.9613498449325562,
                         0.9574459791183472,
                         0.9336588382720947,
                         0.9312138557434082,
                         0.9280960559844971,
                         0.9203505516052246,
                         0.9192730188369751,
                         0.9095813035964966,
                         0.8933322429656982,
                         0.8920265436172485,
                         0.8777315616607666,
                         0.8776772022247314,
                         0.8749797344207764,
                         0.8749552965164185,
                         0.8718560934066772,
                         0.868826150894165]
             }
```

