import os
def displayAccHolders():
	names=[]
	for file in os.listdir(os.getcwd()):
		if file.endswith(".txt"):
			with open(file,'r') as fileobj:
				data=fileobj.readlines()
			names.append(data[1].split(':')[1])
	return names