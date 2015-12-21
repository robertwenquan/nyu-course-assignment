#!/usr/bin/python

"""
The Arithmetic Encoding Method
and Huffman Encoding Method

Robert Wen <robert.wen@nyu.edu>
"""

import logging


class EncArith(object):
  """ arithmetic encoding and decoding"""

  def __init__(self, charset, probset):
    self.charset = charset
    self.probset = probset
    assert(len(self.charset) == len(self.probset))

    self.rangeset = {}
    start = end = 0
    for ch, prob in zip(self.charset, self.probset):
      end += prob
      self.rangeset[ch] = {'startrange':start, 'endrange':end}
      start += prob
    self.rangeset[ch].update({'endrange':1.000})

    logging.debug('charset %s', zip(self.charset, self.probset))
    logging.debug('range set %s', self.rangeset)

  def encode(self, string):
    start = 0
    end = 1

    # get the range
    for ch in string:
      span = end - start
      end = start + span * self.rangeset[ch]['endrange']
      start = start + span * self.rangeset[ch]['startrange']
      logging.debug('%c %f %f', ch, start, end)

    # range to code points
    bin_enc_start = 0
    bin_enc_end = 1

    bit = 0
    encnum = 0
    codepoint = []
    while 1:
      bit += 1
      mid = (bin_enc_end + bin_enc_start)/2.0
      if mid > end:
        bin_enc_end = mid
        codepoint.append('0')
        continue
      elif mid < start:
        bin_enc_start = mid
        codepoint.append('1')
        encnum += pow(2, -1*bit)
        continue
      else:
        break

    return ''.join(codepoint)

  def decode(self, codepoint):
    pass

def main():
  print 'main function'

  logging.basicConfig(level=logging.DEBUG)

  charset = list('ACEKLY')
  probset = [1/8.0, 5/48.0, 5/16.0, 1/8.0, 1/24.0, 7/24.0]
  charset.reverse()
  probset.reverse()

  arith = EncArith(charset, probset)

  print 'original str:', 'KEY'
  encoded_str = arith.encode('KEY')
  print 'encoded  str:', encoded_str
  decoded_str = arith.decode(encoded_str)
  print 'decoded  str:', decoded_str

if __name__ == '__main__':
  main()

