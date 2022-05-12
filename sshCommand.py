import pexpect
#NOTE: DOES NOT WORK BC I DO NOT ACTUALLY KNOW THE PASS
PROMPT = ['# ', '>>> ', '> ', '\$ ']

def send_command(child, cmd):					#used to send commands to shell after authorization
	child.sendline(cmd)
	child.expect(PROMPT)
	
	print(child.before)
	
def connect(user, host, password):  										#returns a spawned ssh connection
	ssh_newkey = 'Are you sure you want to continue connecting'
	connStr = 'ssh ' + user + '@' + host
	child = pexpect.spawn(connStr)											#spawns a child application to tell what to input and expect
	ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])		#expects either a timout, new key, or password prompt (number value determined by index)
	
	if ret == 0:															#timeout
		print('[-] Error Connecting')
		return
	if ret == 1:															#new key  
		child.sendline('yes')												#sends 'yes' to cmd in order to continue
		ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
		"""
		if ret == 0:															#timeout
			print('[-] Error Connecting')
			return
			"""
	else:								#patch to make code work
		print('[-] Error Connecting')
		exit(0)
	
	child.sendline(password)
	child.expect(PROMPT)
	
	return child
	
def main():
	host = 'localhost'
	user = 'root'
	password = 'toor'
	child = connect(user, host, password)
	send_command(child, 'cat /etc/shadow | grep root')
	
if __name__ == '__main__':
	main()
	
	
	
	
	
	
	
	
	
	
	
"""
	if ret == 1:															#new key  
		child.sendline('yes')												#sends 'yes' to cmd in order to continue
		ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
	if ret == 0:															#timeout
		print('[-] Error Connecting')
		return
"""
