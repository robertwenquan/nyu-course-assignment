#!/usr/bin/python

import sys
from scapy.all import *

pkt = IP(dst="192.168.56.1", proto=(1,254))

ans, unans = sr(pkt, timeout = 3)

for s, r in ans:
  r.show()

