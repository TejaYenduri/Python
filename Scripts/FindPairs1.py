def find_pairs(l, num):
    d = {}
    pair_count = 0

    for i in l:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1

    for i in l:
        if (num - i) == i and d[i] == 1:
            pass

        elif (num - i) in d and d[num - i] != 0:
            pair_count += 1
            d[i] -= 1

    print pair_count
    return pair_count


find_pairs([2, 1, 1, 3, 4], 4)
find_pairs([3, 2, 3, 2, 2], 5)
