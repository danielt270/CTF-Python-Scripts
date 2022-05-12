import crypt

def TestPass(cryptPass):
	salt = cryptPass[0:2]						#strips out the salt from the first two characters
	dictFile = open('/media/sf_Shared/ch1/dictionary.txt', 'r')
	for word in dictFile:
		word = word.strip('\n')				#strips the newline character out of the word
		cryptWord = crypt.crypt(word, salt)
		if cryptWord == CryptPass:
			print("[+] Found Password: " + word + "\n"
			return
	print "[-] Password Not Found.\n"
	return
	
def main():
	passFile = open('/media/sf_Shared/ch1/passwords.txt')
	for line in passFile.readlines():
		if ":" in line:
			user = line.split(":")[0]			#splits into array then returns the first element
			cryptPass = line.split(":")[1].strip(' ')
			print("[*] Cracking Password For: " + user
			TestPass(cryptPass)			
if __name__ == "__main__"
	main()
