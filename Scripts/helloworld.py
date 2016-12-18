#helloworld.py
x=int(raw_input("Enter an integer : "))
if x<0:
	x=0
	print 'x value changed to zero'
elif x==0:
	print 'x value is zero'
elif x==1:
	print 'x value is single'
else:
	print 'x value is greater than 1'

