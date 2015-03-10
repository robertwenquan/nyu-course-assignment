#!/usr/bin/python

import sys
from scapy.all import *

pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.56.101/32")
ans,unans = srp(pkt, timeout=3, iface="p7p1")

for s, r in ans:
  print r.sprintf("%Ether.src% %ARP.psrc%")
  r.show()

for s in unans:
  s.show()
