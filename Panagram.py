'''
A pangram is a sentence that contains all the letters of the English alphabet at least once, for example: The quick brown fox jumps over the lazy dog. Your task here is to write a function to check a sentence to see if it is a pangram or not.
'''
def is_panagram(inputStr):
	d= dict.fromkeys('abcdefghijklmnopqrstuvwxyz',0)
	for i in inputStr:
		if(d.has_key(i)):
			d[i] = 1
	for i in d:
		if d[i] != 1:
			print "not a panagram"
			return False

	print "is a panagram"
	return True
is_panagram('The quick brown fox jumps over the lazy dog.')	


		

