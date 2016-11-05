def is_vowel(char):
	if(type(char) != str):
		print "invalid input"
		return False
	if(len(char) == 1):
		d = dict.fromkeys('aeiou',0)
		if(d.has_key(char)):
			print "given char is vowel"
			return True
		else:
			print "not a vowel"
			return False
	else:
		print "given more than one character as input"
		return False
is_vowel('a')
