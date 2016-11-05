def is_palindrome(inputStr):
	size = len(inputStr)
	if(size == 0):
		return False
	else:
		index2 = size-1;
		for index1 in range(size):
			if(inputStr[index1].lower() != inputStr[index2].lower()):
				return False
			else:
				index2 -= 1
		return True

truthValue = is_palindrome('Mom')
print truthValue
