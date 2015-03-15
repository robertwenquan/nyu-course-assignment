#!/usr/bin/python

import json
import time
import urllib
import hashlib
import requests
from PIL import Image
from StringIO import StringIO
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol
from utils.fingerprint import fingerprint
from utils.fingerprint import compact_fingerprint_path

from storage.managers import S3StorageManager


class MRLogConvert(MRJob):

  OUTPUT_PROTOCOL = RawValueProtocol


  def __init__(self, args):

    super(MRLogConvert, self).__init__(args)

    self.s3_bucket = 's3://clarifai-crawl'
    self.s3_key = 'AKIAJ3YY2AJPNVQH4E2A'
    self.s3_secret = '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'

    self.crawler = "flickrcc"

    self.s3manager = S3StorageManager(self.s3_bucket, self.s3_key, self.s3_secret)


  def mapper(self, _, line):

    line = urllib.unquote(line.strip()).decode('utf8')
    fields = line.split("\t")

    # 0.  * Photo/video identifier
    # 1.  * User NSID
    # 2.  * User nickname
    # 3.  * Date taken
    # 4.  * Date uploaded
    # 5.  * Capture device
    # 6.  * Title
    # 7.  * Description
    # 8.  * User tags (comma-separated)
    # 9.  * Machine tags (comma-separated)
    # 10. * Longitude
    # 11. * Latitude
    # 12. * Accuracy
    # 13. * Photo/video page URL
    # 14. * Photo/video download URL
    # 15. * License name
    # 16. * License URL
    # 17. * Photo/video server identifier
    # 18. * Photo/video farm identifier
    # 19. * Photo/video secret
    # 20. * Photo/video secret original
    # 21. * Photo/video extension original
    # 22. * Photos/video marker (0 = photo, 1 = video)

    if fields[22] == "1":
      return

    if fields[14] == "" or fields[14] == None:
      return

    item = dict()

    item['crawler'] = 'flickrcc'
    item['crawlers'] = ['flickrcc']
    item['url'] = fields[14]
    item['image_urls'] = [fields[14]]

    item['flickr_photoid'] = fields[0]
    item['flickr_userid'] = fields[1]

    item['flickr_date_taken'] = fields[3]
    item['flickr_date_posted'] = fields[4]

    if fields[6] != "":
      item['title'] = fields[6]

    if fields[7] != "":
      item['flickr_desc'] = fields[7]

    if fields[8] != "":
      item['labels'] = fields[8].split(",")

    if fields[10] != "":
      item['flickr_longitude'] = fields[10]

    if fields[11] != "":
      item['flickr_latitude'] = fields[11]

    item['ref_urls'] = [fields[13]]

    item['flickr_license'] = fields[15]

    # download image
    r = requests.get(item['url'])

    # NOTE:
    # There is an image conversion step in scraper, for compression. Let's ignore it
    # This will result in faster conversion as well as better image quality
    #i = Image.open(StringIO(r.content))

    # get the MD5 hash for the image
    item['md5'] = hashlib.md5(StringIO(r.content).read()).hexdigest()

    # docid is the fingerprint of the picture url
    item['docid'] = fingerprint(item['url'])

    bucket = self.s3_bucket
    base = "img/%s" % self.crawler
    fileloc = compact_fingerprint_path(item['url'])

    # fill in the s3_path according to the base store, crawler, docid and file type
    s3_path = "%s/%s/%s" % (bucket, base, fileloc)
    item['s3_path'] = s3_path

    # store the image into S3
    if self.s3manager.exists(s3_path) == False:
      self.s3manager.s3_bucket.write_file(s3_path, StringIO(r.content))

    # store timestamp in ms
    item['timestamp_ms'] = int(time.time() * 1000)

    yield None, "%s\t%s" % (item['docid'], json.dumps(item, separators=(', ',': ')))


if __name__ == '__main__':
  MRLogConvert.run()

