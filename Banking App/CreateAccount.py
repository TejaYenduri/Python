import random
def create_account():
	account_no = random.randint(100,1000)
	name = raw_input("Enter your name")
	address = raw_input("Enter your address")
	phone = raw_input("Enter your phone number")
	balance = 500

	file_name = str(account_no)+'.txt'
	file_object= open(file_name,'w')
	file_object.write("AccountNumber:"+str(account_no)+"\n")
	file_object.write("Name:"+name+"\n")
	file_object.write("Address:"+address+"\n")
	file_object.write("Phone:"+phone+"\n")
	file_object.write("Balance:"+str(balance)+"\n")
	file_object.close()
	return account_no

