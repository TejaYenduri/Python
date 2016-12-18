import string
inputStr= raw_input("enter word as any sequence of one or more lower-case letters(no numbers or punctuation)")
wordList = inputStr.split()

print "Number of words in the input", len(wordList)
wordList.sort()
print "Words:"
for word in set(wordList) :
	print word,wordList.count(word)
print "Letters:"
for i in string.lowercase[:26] :
	print i,inputStr.count(i)