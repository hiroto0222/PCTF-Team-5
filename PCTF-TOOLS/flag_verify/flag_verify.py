from os import listdir
from os.path import isfile
from FlagObj import *
import socket
from  _thread import *
from datetime import datetime

'''------------------------------------------------------------------------------------------------------------------
 ' Flag checker for CTF
 '
 '
 ' Description: This application is a standalone server that listens on a port. This application will first read
 '		all flags, flag IDs, and flag passwords for current service. An incoming message from MITM proxy.
 '		If outgoing message contains valid flag password or flag then the input is checked to see if
 '		valid flag password, flag ID pair is sent. If not then flag password or flag was sent by exploit
 '		Logic and return values:
 '		if valid flag password or flag are detected in output. Get Flag ID.
 '		then, check if matching flag ID with flag password or flag are detected in input.
 '		if so, return "1" else return "0"
 '
 ' Instructions: Be sure to fill out configuration for service such that this application can read flags
 '		 correctly. If 0 flags read return "1" automatically. Once configuration is filled check to see
 ' 		 if flags could be read under current user. If so, then just run and ready to go. If not then
 '		 this application will need to be ran through the MITM proxy called by Xinetd.d that runs under
 '		 user that *should* be the owner of flags.
 '
 '
 ' !!!!!!!!!!!!!!!!WARNING: THIS APPLICATION MIGHT BE CPU INTENSIVE, IF SO DO NOT USE DURING CTF.!!!!!!!!!!!!!!!!
 '
-----------------------------------------------------------------------------------------------------------------'''


# Configure for specific service. ##################################################################################
FLAG_PATH = "/opt/ctf/backup/append/"

PORT = 30001

DEBUG = 1

SPLIT_STR = ":__SpLiT__:"

FLAG_TAG = "FLG"
####################################################################################################################

# Print debug statements.
def debug(msg):
	if (DEBUG):
		print ("Debug: " + msg)

def getFlags():
	flags = []
	count = 0
	for f in listdir(FLAG_PATH):
		flag = ""
		flagId = ""
		flagPass = ""
		if isfile(FLAG_PATH + f):
			splitStr = f.split("_")
			if len(splitStr) == 2:
				flagId = splitStr[0]
				splitStr = splitStr[1].split(".")
				if len(splitStr) == 3:
					flagPass = splitStr[0]
					try:
						file = open(FLAG_PATH + flagId + "_" + flagPass + ".secure.bak", "r")
						flag = file.read().strip()
						file.close()
						if FLAG_TAG in flag:
							flags.append(FlagObj(flagId, flagPass, flag))
					except:
						print ("File not found: " + flagId + "_" + flagPass + ".secure.bak")
						continue
		count+=1


	print ("flags found: " + str(len(flags)) + ", count: " + str(count))
	return flags

def checkIO(userIn, userOut, flags):
	for flag in flags:
		if flag.flag in userOut  or flag.flagPass in userOut:
			print("Flag: " + flag.flag)
			print("flagPass: " + flag.flagPass)
			print("FlagID: " + flag.flagId)
			if flag.flag in userIn or flag.flagPass in userIn:
				return "0"
			else:
				return "1"
	return "0"


def clientThread(conn, flags):
	data = ""
	try:
		conn.settimeout(2)
		tempRecv = conn.recv(1024)
		while tempRecv:
			data += tempRecv
			conn.settimeout(0.1)
			tempRecv = conn.recv(1024)
	except socket.timeout:
		if (data==""):
			print "timed out."
	except:
		print "Error:"

	if (data != ""):
		splitStr = data.decode().split(SPLIT_STR)
		if len(splitStr) == 2:
			userIn = splitStr[0]
			userOut = splitStr[1]

			# Check flag
			reply = checkIO(userIn, userOut, flags)
			print "Received: " + userIn + ", " + userOut
			print "Replied: " + reply
			conn.send(reply)
	print ("closed")
	conn.close()

def main():
	flags = getFlags()
	try:
		s = socket.socket()
		print "Socket successfully created"

		s.bind(('', PORT))
		print "socket binded to %s" %(PORT)
	except socket.error:
		print ("Binding socket failed")

	s.listen(5)

	# Continuously listen for connections. Then spawn new thread.
	while True:
		c, addr = s.accept()
		print ("*" + str(datetime.now()) + "*")
		print "Got connection from", addr
		# Do stuff.
		start_new_thread(clientThread, (c,flags,))

main()
