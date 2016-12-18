'''Write a program that given a text file will create a new text file
in which all the lines from the original file are numbered from 1 to n
(where n is the number of lines in the file).
'''
import os
def number_linesin_file():
    """function to create new text file with numbers"""
    filename = raw_input(" enter text file name  ")
    # check whether file exists or not. if exists, check if its not empty
    if os.path.isfile(filename) and os.stat(filename).st_size != 0:
        #variable used for writing line numbers in new file
        linenumber = 1
        #creating a new text file with name as 'new' appending to original file
        new_file_name = 'new'+filename
        fileobj = open(new_file_name, 'w')
        try:
            for line in open(filename, 'r'):
                newline = str(linenumber)+ ' '+line
                fileobj.write(newline)
                linenumber += 1
        except IOError as io_error:
            code, message = io_error.args
            print code, message
        finally:
            fileobj.close()
    else:
        print "no such file"
number_linesin_file()
