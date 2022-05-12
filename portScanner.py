import argparse
import socket
from socket import *
from threading import *

screenLock = Semaphore(value=1)								

def connScan(tgtHost, tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)				#defines the protocol and socket types
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send("ViolentPython\r\n")
		results = connSkt.recv(100)							#grabs the banner with the (arg is buffer size)
		screenLock.acquire()								#locks the thread from printing anything
		
		print("[+] %d/tcp open" %tgtPort)					#because the thread is locked, these print statements would be the only ones outputted
		print("[+] " + str(results))						#when threading you need to screen lock before printing or else you would get a jumble of words becuase of the multiple threads
	except:
		screenLock.acquire()														
		print("[-] %d/tcp closed" %tgtPort)
	finally:												#finally is always executed regardless if there is an exception
		screenLock.release()								#releases the lock for the threading to continue
		connSkt.close()
		
		
def portScan(tgtHost, tgtPorts):									#determines if host can be resolved, if so it goes on to try to connect to the specified ports
	try:
		tgtIP = gethostbyname(tgtHost)								#takes a hostname (i.e. www.google.com) and returns its IPv4
	except:
		print("[-] Cannot resolve '%s': Unknown host" %tgtHost)
		return
	
	try:
		tgtName = gethostbyaddr(tgtIP)								#takes a IP addr and returns a triple containing the hostname, alternative list of host names, and a list of IPv4/v6 addresses
		print("\n[+] Scan Results for: " + tgtName[0])
	except:
		print("\n[+] Scan Results for: " + tgtIP)
	
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
		t.start()
		"""
		print("Scanning port " + tgtPort)
		connScan(tgtHost, int(tgtPort))
		"""
		

def main():           	
	parser = argparse.ArgumentParser(description='Scans for specific ports from a given IP and returns the status')	#creates parser and adds description
	parser.add_argument("-H", required=True, help="specify target host")											#defines variables for the switches (type defaults to string)
	parser.add_argument("-p", required=True, nargs="+", help="specify target port(s)")           					#regex is used for nargs (# of args)         
	args = parser.parse_args()																						#equivalent to '(options, args) = parser.parse_args()'
																					
	tgtHost  = args.H
	tgtPorts = args.p
	
	portScan(tgtHost, tgtPorts)
	
if __name__ == "__main__":
	main()
	
	

