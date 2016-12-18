def find_pairs(l, num):
    #d = {}
    pair_count = 0
    '''
    for i in l:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    '''
    for i in l:
        if abs(num - i) in l:
            pair_count += 1
            l.remove(i)
    print pair_count
    return pair_count


find_pairs([2, 1, 1, 3, 4], 4)
