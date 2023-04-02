#!/usr/bin/env python

import re
import subprocess
import sys

HEADER = 53

# accept input
if (len(sys.argv) > 2):
    print("accepts only one .pcap file")
    exit()
elif (len(sys.argv) == 1):
    print("accepts one .pcap file")
else:
   filename = sys.argv[1]

command = 'tcpdump'
param = '-Aqr'  # -A     Print each packet (minus its link level header) in ASCII.
                # -q     Print less protocol information so output lines are shorter.
                # -r     Read packets from file

pcap_raw = subprocess.check_output([command, param, filename])
pcap = pcap_raw.decode('utf-8')
packets = re.split('\n(?=\d\d:\d\d)', pcap)
print('\n')

for packet in packets:
    print(packet)
    lines = packet.splitlines()
    headline = lines[0]
    offset = len(headline)

    time_stamp = packet[:15]
    src_port = re.search('(?<=\.)(?:(?!\.).)*?(?=\ >)', headline).group(0)
    src_ip = re.search('(?<=IP )(?:(?!IP ).)*?(?=\.%s)' % (src_port), headline).group(0)
    dst_port = re.search('(?<=\.)(?:(?!\.).)*?(?=\:)', headline).group(0)
    dst_ip = re.search('(?<=\> )(?:(?!\> ).)*?(?=.%s)' % (dst_port), headline).group(0)
    payload = packet[(offset + HEADER):]
    data = '\n||\t\t\t\t'.join(payload.splitlines())

    with open("MONITORED_TRAFFIC.txt", "a") as myfile:
        myfile.write('|| Src. IP: \t%s' % (src_ip))
        myfile.write('|| Src. port: \t%s\n' % (src_port))
        myfile.write('|| Dst. IP: \t%s' % (dst_ip))
        myfile.write('|| Dst. port: \t%s\n' % (dst_port))
        myfile.write('|| Time: \t\t%s\n' % (time_stamp))
        myfile.write('|| Data: \t\t%s\n' % (data))
        myfile.write('========================== = = = = =  =  =  =  =   =   =   ~    ~    -    -\n')
