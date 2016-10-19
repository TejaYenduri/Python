import CreateAccount
import Withdraw
import Deposit
import DisplayAccHolders
import Delete

choice=input("Enter your choice as number"
	          "1: CreateAccount"
	          "2: Withdraw"
	          "3: Deposit"
	          "4: Delete "
	         )
if choice ==1:
	account=CreateAccount.create_account()
	print "Your account number ",account
elif choice==2:
	acctNo= input("enter account number ")
	amt=input("enter amount to withdraw ")
	stmt=Withdraw.withdraw_cash(acctNo,amt)
	print str
elif choice==3:
	acctNo= input("enter account number ")
	amt=input("enter amount to deposit ")
	stmt=Deposit.deposit_cash(acctNo,amt)
	print str

elif choice==4:
else:
	print "choose from given options"