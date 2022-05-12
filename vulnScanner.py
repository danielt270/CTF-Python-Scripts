import socket
import os
import sys

def RetBanner(ip, port):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((ip, port))
		banner = s.recv(1024)		#number of bytes (characters) to capture
		return str(banner)
	except:
		return
	
def CheckVulns(banner, fileName):
	f = open(fileName, "r")
	for line in f.readlines():
		if line.strip('\n') in banner:						#strip('\n') makes sure each line is single spaced (otherwise prints out double)
			print("[+] Server is vulnerable: " + banner.strip("ready. \\r\\n\'").strip('b\'220 '))	
						
def main():	
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		if not os.path.isfile(filename):			#checks if file exists
			print("[-] " + filename + " does not exist.")
			exit(0)						#closes the program without errors
		if not os.access(filename, os.R_OK):			#checks if user has the appropraiate permissions
			print("[-] " + filename + " access denied.")
			exit(0)
		print('-' * 100 + '\n' + "[+] Reading Vulnerabilities From: " + filename + '\n' + '-' * 100)
	else:
		print("[-] Usage: " + str(sys.argv[0]) + " <vuln filename>")	#prints if no filename is given
		exit(0)
		
	portList = [21, 22, 25, 80, 110]	
	for x in range(102, 103):
		ip = "192.168.1." + str(x)
		for port in portList:
			print("Checking " + ip + ":" + str(port))
			banner = RetBanner(ip, port)											
			if banner:
				CheckVulns(banner, filename)			
			else:
				print("[-] port is not open")

if __name__ == "__main__":
	main()
		
