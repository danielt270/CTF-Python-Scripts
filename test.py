"""
str1 = "b[+] 0.0.0.0: \'220 pyftpdlib 1.5.6 ready.\\r\\n\'"

print(str1)
#print(str1.strip("\\r\\n\'"))
print(str1.strip("b\\r\\n\'"))
"""


f = open("/media/sf_Shared/CH1/vuln-banners.txt", "r")
for line in f.readlines():
	print(line.strip('\n'))
