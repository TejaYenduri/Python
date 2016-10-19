import CreateAccount
import Withdraw
import Deposit
import Delete
import DpAccHolders

choice=input("Enter your choice as number"
	          "1: CreateAccount"
	          "2: Withdraw"
	          "3: Deposit"
	          "4: Delete "
	          "5: Display Account Holders"
	         )
if choice ==1:
	account=CreateAccount.create_account()
	print "Your account number ",account
elif choice==2:
	acctNo= input("enter account number ")
	amt=input("enter amount to withdraw ")
	stmt=Withdraw.withdraw_cash(acctNo,amt)
	print stmt
elif choice==3:
	acctNo= input("enter account number ")
	amt=input("enter amount to deposit ")
	stmt=Deposit.deposit_cash(acctNo,amt)
	print stmt

elif choice==4:
	acctNo= input("enter account number ")
	stmt=Delete.delete(acctNo)
	print stmt
elif choice==5:
	names=DpAccHolders.displayAccHolders()
	for i in names:
		print i
else:
	print "choose from given options"