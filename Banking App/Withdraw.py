import os.path

def withdraw_cash(acctNo,amt):
	file_name=str(acctNo)+".txt"
	stmt=''
	if os.path.isfile(file_name):
		with open(file_name,'r') as fo:
			data=fo.readlines()
		bal= int(data[4].split(':')[1])
		
		if(bal>=amt):
			bal-=amt
		else:
			stmt="Amount entered exceeds balance"
		data[4]='Balance:'+str(bal)
		with open(file_name,'w') as fo:
			fo.writelines(data)
		stmt="Your current bal: ",bal
		
	else:
		stmt="no such account"
	return stmt
	
		


