#!/usr/bin/python

import sys
from scapy.all import *

IPLIST=["10.20.111.0", "10.20.111.1", "10.20.111.2", "10.20.111.3"]
PKTS=[]


for ip in IPLIST:
  ippkt=IP(dst=ip)
  for port in [80,53]:
    l3=ippkt/TCP(dport=port)
    l2=Ether()/l3

    PKTS.append(l2)

for pkt in PKTS:
  pkt.show()

