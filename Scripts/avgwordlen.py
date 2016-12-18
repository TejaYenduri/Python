'''Write a program that will calculate the average word length of a text
stored in a file (i.e the sum of all the lengths of the word tokens in the
text, divided by the number of word tokens).'''
import os
import string
def avg_wordlen_in_file():
    """function to calculate average word length in a given text file"""
    filename = raw_input(" enter text file name with extension  ")
    # check whether file exists or not. if exists, check if its not empty
    if os.path.isfile(filename) and os.stat(filename).st_size != 0:
        sum_of_lengths = 0
        number_of_words = 0
        try:
            for line in open(filename, 'r'):
                #splitting each line by space in file to get individual words
                for word in line.split():
                    #removing punctuation in the words
                    word = word.translate(None, string.punctuation)
                    #adding the lengths of words
                    sum_of_lengths += len(word)
                    number_of_words += 1
            print "sum of lengths ", sum_of_lengths
            print "number of words ", number_of_words
            avg_word_len = sum_of_lengths/number_of_words
            print avg_word_len
            return avg_word_len
        except IOError as io_error:
            code, message = io_error.args
            return -1
    else:
        print "no such file"
        return -1
avg_wordlen_in_file()
