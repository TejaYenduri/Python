''' Write a program that maps a list of words into a list of integers
representing the lengths of the correponding words. Write it in three
different ways: 1) using a for-loop, 2) using the higher order function map(),
and 3) using list comprehensions. '''

def forMaps(wordsList):
	wordLength=[]
	#only if length of list is greater than or equal to 1 it enters the for loop
	if (len(wordsList) >=1):
		for word in wordsList:
			# computes length only for strings and ignores any other data type
			#if (type(word)==str):
				#wordMap[word] = len(word)
			wordLength.append(len(word))
		#print wordMap
		print wordLength
	#return wordMap
	return wordLength
forMaps(['hello','hi there','how'])

'''
def wordLength(word):
	if(type(word)==str):
		return len(word)
	else:
		return 0
'''
def usingMap(wordList):
	
	print list(map(lambda word:len(word),wordList))
	
usingMap(['hello','hi there','how'])

def usingListCom(wordList):
	wordLength = [len(word) for word in wordList]
usingMap(['hello','hi there','how'])