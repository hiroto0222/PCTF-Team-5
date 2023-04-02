# PCTF-Team-5
Collection of created tools/scripts for CTF

## Usage
PCTF-Tools/SWAPG provided by the instructor.

### Backdoor (PCTF-TOOLS/backdoorv2)
``` 
$ python backdoor_connect.py
```
- Proper Game IP and Auth token required.
- Change `INFECTED_HOSTS` and `HOSTS_IP` during CTF.

### Traffic Analyzer (PCTF-TOOLS/traffic_analyzer)
The `traffic_monitor.bash` executes `tcpdump` command every 3 min (180 sec), saves `.pcap` file, and repeats until manually stopped
```
$ ./traffic_monitor.bash
```
The `packet_analyer.py` takes `.pcap` file as input argument, and outputs

`MONITORED_TRAFFIC.txt` file with all packets.
```
$ python packet_analyer.py <filename.pcap>
```
