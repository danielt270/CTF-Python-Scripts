import zipfile
import optparse
from threading import Thread

def ExtractFile(zFile, password):
	try:
		zFile.extractall(pwd=password)
		print("[+] Found password = " + password + '\n')
	except:
		pass

def main():
	parser = optparse.OptionParser("usage%prog -f <zipfile> -d <dictionary>")			#displays how the program is used
	parser.add_option('-f', dest='zname', type='string', help='specify zip file')
	parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
	(options, args) = parser.parse_args()
	
	if options.zname == None or options.dname == None:						#makes sure the arguments are used
		print parser.usage
		exit(0)
	else:
		zname = options.zname
		dname = options.dname
		
	zFile    = zipfile.ZipFile(zname)
	passFile = open(dname)   			

	for line in passFile.readlines():
		password = line.strip('\n')	
		t        = Thread(target=ExtractFile, args=(zFile, password))
		t.start()

if __name__ == "__main__":
	main()
