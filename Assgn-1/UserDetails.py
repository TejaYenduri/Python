import datetime
#accesing user details and displaying the year that user will turn 80
name = raw_input("enter your name ")
age = input("enter your age  ")

now = datetime.datetime.now()
if age < 80 :
	ageDiff = 80-age
	print "you will turn 80 in the year", now.year+ageDiff


