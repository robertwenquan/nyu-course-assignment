"""
tag the image samples, and extract the visual feature as well

input: a line based JSONL file, each line representing one image
output: image url, with predicted labels and feature vectors
"""

import os
import sys
import json
import logging
from clarifai.client import ClarifaiApi
from utils import Worker

class imageTag(object):

  fio_r = fio_w = None
  api = None
  images = []

  def __init__(self, input_filename, output_filename):

    self.fio_r = open(input_filename, 'r')
    self.fio_w = open(output_filename, 'wb')
    self.api = ClarifaiApi(model='general-v1.3')

  def read_images(self):
    """ read in image samples """

    lines = self.fio_r.readlines()
    logging.debug('%d lines read' % len(lines))

    items = []
    for line in lines:
      line = line.strip()
      try:
        item = json.loads(line)
      except:
        continue
      items.append(item)

    self.images = items
    logging.debug('%d images have been read' % len(items))

  def tag_images(self):
    """ get the labels and features of the images """

    worker = Worker(50)

    for image in self.images:
      worker.add_task(self.tag_image, image)

    worker.join()

  def tag_image(self, image):
    """ tag and embed one image """

    imageurl = image.get('url')
    if not imageurl:
      return

    try:
      result = self.api.tag_and_embed_urls(imageurl)

      image['tags'] = result['results'][0]['result']['tag']['classes']
      image['probs'] = result['results'][0]['result']['tag']['probs']
      image['embeds'] = result['results'][0]['result']['embed']
    except:
      logging.error('FAILED %s' % imageurl)

    print 'FINSHED %s' % imageurl
    self.fio_w.write(json.dumps(image) + '\n')

  def run(self):
    """ run the tag service """

    self.read_images()

    self.tag_images()

#
# main routine
#
def main():

  input_filename = sys.argv[1]
  output_filename = sys.argv[2]

  logging.basicConfig(level=logging.DEBUG)
  logging.info('input: %s' % input_filename)
  logging.info('output: %s' % output_filename)

  if input_filename is None:
    raise Exception('arguments wrong. Please specify input filename')

  if output_filename is None:
    output_filename = 'results.jsonl'

  if not os.path.exists(input_filename):
    raise Exception('%s file not exist.' % input_filename)

  img_tagger = imageTag(input_filename, output_filename)
  img_tagger.run()


if __name__ == '__main__':
  main()

