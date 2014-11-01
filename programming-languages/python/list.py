#!/usr/bin/python

post = dict()
post['tags'] = ['abc', 'bcd', 'ss', 'eewe', 'sdfdf', 'cat', 'dog']
print post

for tag in post['tags']:
  print tag

aa = [tag for tag in post['tags']]
print aa
