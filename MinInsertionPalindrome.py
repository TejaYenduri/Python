# coding=utf-8
'''
Given a string, find the minimum number of characters to be inserted to convert it to palindrome.
For Example:
ab: Number of insertions required is 1. bab or aba
aa: Number of insertions required is 0. aa
abcd: Number of insertions required is 3. dcbabcd
Input:

The first line of input contains an integer T denoting the number of test cases.
The first line of each test case is S.

Output:

Print the minimum number of characters.

Constraints:

1 ≤ T ≤ 50
1 ≤ S ≤ 40
'''


def find_min_insertions(input_str, start_index, end_index):
    if start_index > end_index:
        return -1
    if start_index == end_index:
        return 0
    if start_index == end_index - 1:
        if input_str[start_index] == input_str[end_index]:
            return 0
        else:
            return 1
    if input_str[start_index] == input_str[end_index]:
        return find_min_insertions(input_str, start_index + 1, end_index - 1)
    else:
        return min(find_min_insertions(input_str, start_index, end_index - 1),
                   find_min_insertions(input_str, start_index + 1, end_index)) + 1


def read_input():
    print "input:"
    test_cases = input("enter number of testcases  ")
    input_str = []
    for i in range(test_cases):
        input_str.append(raw_input("enter the string  "))
    print "output:"
    for i in range(test_cases):
        if input_str[i] != "":
            number = find_min_insertions(input_str[i], 0, len(input_str[i]) - 1)
            print number


read_input()
