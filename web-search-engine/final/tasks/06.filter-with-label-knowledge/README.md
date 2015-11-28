### Objective

Based on the image samples and assosiated label knowledge, filter the irrelevant samples

### How
generate knowledge graph based on predicted labels
use is-a is-not relationship to filter irrelevant items

For example, the predicted labels are [l1, l2, l3], the ground truth is l1, so the item will be kept.
If the ground truth is l4 but l4 IS-A l1, like dog IS-A animal. Then the item will be kept.
Or if any one of [l1, l2, l3] is the synonyms of l4, the item will be kept as well.

If there is no relation of l4 to [l1, l2, l3], the item will be filtered.

### Input
A set of images
Associate meta data of these images

### Deliverable
A subset of the images and the associated meta data

