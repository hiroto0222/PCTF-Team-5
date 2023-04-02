#!/bin/bash
# runs tcpdump every 3 mins and writes to tcpdump_out[i].pcap

i="1"

while true; do
echo "running tcpdump..."
tcpdump -i eth0 -Aqn -w tcpdump_out$i.pcap & pid=$!
sleep 180
kill $pid
echo "tcpdump terminated"
i=$[$i+1]
done
