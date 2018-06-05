import itertools

match_result_label_vtx = {0: [1, 2, 3, 4], 1: [5, 6], 2: [7]}
Chd_label_count = {0: 3, 1: 2, 2: 1}
frist = True
permutations = []
for key, value in match_result_label_vtx.iteritems():

    if frist:
        n = Chd_label_count[key]
        for i in itertools.permutations(value, n):
            item = {key: [j for j in i]}
            permutations.append(item)
        # permutations=per
        # print key
        # print n
        # print value
        # print permutations
        frist = False
    else:
        n = Chd_label_count[key]
        per = list(itertools.permutations(value, n))

        product = list(itertools.product(per, permutations))
        print(product)
        new_permutations = []
        for i in product:
            print "i:",i
            item = i[1]
            print item
            print i[0]
            item[key] = [j for j in i[0]]
            new_permutations.append(item)
           # print item
        permutations=new_permutations
        # print key
        # print permutations
        # print "-----"
        # print new_permutations