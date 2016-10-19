import os
def delete(acctNo):
	file_name=str(acctNo)+".txt"
	stmt=''
	if os.path.isfile(file_name):
		os.remove(file_name)
		stmt=str(acctNo)+"  deleted"
	else:
		stmt="No such account"
	return stmt