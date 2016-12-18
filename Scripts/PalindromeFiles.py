'''
Write a version of a palindrome recogniser that accepts a file name from the user, reads each line, and prints the line to the screen if it is a palindrome.
'''
import os
import string
def palindromeFiles():
	fileName = raw_input("Enter file name with extension ")
	if (fileName == None): print "invalid file name"
	if os.path.isfile(fileName):
		try:
			fileObject = open(fileName,'r')
			lineList = fileObject.readlines()
			for line in lineList:
				isPalindrome = is_palindrome(line)
				if(isPalindrome):
					print line
		except IOError as ie:
			code,message = ie.args
			print code,message
			
	else:
		print "no such file"

def is_palindrome(inputStr):
	punctuationSet = set(string.punctuation)
	modifiedStr = "".join(c for c in inputStr if c not in punctuationSet)
	modifiedStr = modifiedStr.translate(None,string.whitespace)
	size = len(modifiedStr)
	if(size == 0):
		return False
	else:
		index2 = size-1;
		for index1 in range(size):
			if(modifiedStr[index1].lower() != modifiedStr[index2].lower()):
				return False
			else:
				index2 -= 1

		return True
palindromeFiles()



