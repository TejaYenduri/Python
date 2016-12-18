#Write a script to print output in the below format
#If the input is  num = 5
#
     #
    ###
   #####
  #######
 #########
#
num = input("Enter a number ")

for i in range(num) :
    print " "*(num-i),'#'*(2*i+1)