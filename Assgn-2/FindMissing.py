def findMissing(list):
	list.sort();
	size= len(list)
	nextInt =0
	for i in range(size):
		if list[i]+1 <0 :
		  continue
		nextInt = list[i]+1
		if i+1 < size and nextInt != list[i+1] :
			if nextInt>0:
				break
			if nextInt==0 and nextInt+1 != list[i+1]:
				nextInt+=1
				break

	return nextInt;

def main():
	list=[-1000,0,1,2,3]
	firstPos=findMissing(list)
	print firstPos
main()