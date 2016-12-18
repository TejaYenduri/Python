'''
Using the higher order function reduce(), write a function max_in_list() that takes a list of numbers and returns the largest one. 
'''

def max(x,y):
	if(x>y):
		return x
	else:
		return y

	 

def max_in_list(list):
	print reduce(lambda x, y: max_in_list(x,y), list)

max_in_list([2,9,-1,6,17])