#!/usr/bin/python

import sys
from scapy.all import *

pkt = IP(dst="192.168.56.1")/TCP(dport=(1025,1335), sport=RandShort())

ans, unans = sr(pkt, timeout=3)

for s,r in ans:
  print r.sprintf("%TCP.sport% %TCP.dport%")

for s in unans:
  s.show()
