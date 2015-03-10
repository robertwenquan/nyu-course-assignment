#!/usr/bin/python

import sys
from scapy.all import *

pkts=IP(dst="10.0.2.2")/TCP(sport=range(11111,11122),dport=111)
send(pkts)

