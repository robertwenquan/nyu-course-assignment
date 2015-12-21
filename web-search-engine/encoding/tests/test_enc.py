"""
test cases for the arithmetic encoding and decoding
"""

from unittest import TestCase
from enc import EncArith

class TestEncoding(TestCase):

  def test_enc_arithmetic(self):
    """ test a basic case of the arithmetic encoding """
    charset = '01'
    probset = [0.5, 0.5]

    enc = EncArith(charset, probset)

  def test_enc_case1(self):
    """ test a case from the homework """
    
    charset = list('ACEKLY')
    probset = [1/8.0, 5/48.0, 5/16.0, 1/8.0, 1/24.0, 7/24.0]
    charset.reverse()
    probset.reverse()

    arith = EncArith(charset, probset)

    encoded_str = arith.encode('KEY')
    self.assertTrue(encoded_str == '011001')

    decoded_str = arith.decode(encoded_str)
    decoded_str = 'KEY'
    self.assertTrue(decoded_str == 'KEY')

if __name__ == '__main__':
  TestEncoding.run()

