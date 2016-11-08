'''
write a code that slices the string (which is an input), append it to a list, count the number of each letter - and if it is identical to the letter before it, don't put it in the list, but rather increase the appearance number of that letter in the one before.
'''
def countLetter(inputStr):
	d={}
	for c in inputStr:
		if not d.has_key(c):
			d[c] = 1
		else : 
			value = d[c]
			value += 1
			d[c] = value
	print d
countLetter('commander')