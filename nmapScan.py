import nmap
import argparse

def nmapScan(tgtHost, tgtPort):
	nmScan = nmap.PortScanner()
	nmScan.scan(tgtHost, tgtPort)
	state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']					#can be state/reason/name for last index
	print(" [*] " + tgtHost + " tcp/" + tgtPort + " " + state)
	
def main():
	parser = argparse.ArgumentParser(description='Scans for specific ports from a given IP and returns the status using nmap')
	parser.add_argument("-H", required=True, help="specify target host")
	parser.add_argument("-p", required=True, nargs="+", help="specify target port(s)")
	args = parser.parse_args()
	
	tgtHost  = args.H
	tgtPorts = args.p
	
	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)
		
if __name__ == '__main__':
	main()
