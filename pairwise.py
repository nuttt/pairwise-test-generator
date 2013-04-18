from copy import copy
from random import seed, shuffle
import sys



def pairwise(params,poolsize=20):
    
    seed(2)
    
    param_values = []
    param_names = []
    param_position = []
    all_values = []

    testsets = []

    # put data across lists
    for param_name, param_value in params:

        param_num = len(param_names)
        param_names.append(param_name)

        # convert param value to id
        value_list = []
        for value in param_value:
            num = len(all_values)
            all_values.append(value)
            value_list.append(num)
            param_position.append(param_num)

        param_values.append(value_list)

    # generate all possible pair and mark of unused pair for searching

    all_pairs_num = 0
    unused_pair_search = []
    unused_count = [0]*len(all_values)

    for i, list1 in enumerate(param_values):

        unused_pair = []

        for j, list2 in enumerate(param_values):
            if i < j:
                for x in list1:
                    unused_count[x] += len(list2)
                for y in list2:
                    unused_count[y] += len(list1)
                all_pairs_num += len(list1) * len(list2)
                unused_pair += [1]*len(list2)
            else:
                unused_pair += [0]*len(list2)

        unused_pair_search += [copy(unused_pair) for _ in range(len(list1))]

    # while some pair have not been crossed

    all_values_num = len(all_values)

    while all_pairs_num > 0:
        
        # pick up best pair
        best_value = -1
        best_pair = (-1,-1)

        for x in range(all_values_num):
            for y in range(all_values_num):
                if not unused_pair_search[x][y]:
                    continue
                value = unused_count[x] + unused_count[y]
                if value > best_value:
                    best_value = value
                    best_pair = (x,y)

        best_x, best_y = best_pair

        # find best testset

        best_testset = []
        best_testset_coverage = -1

        for pool in range(poolsize):

            testset = [best_x, best_y]

            # generate order for finding more pair
            param_x = param_position[best_x]
            param_y = param_position[best_y]
            orders = [param_x, param_y]
            remain = [i for i in range(len(param_names)) if i != param_x and i != param_y]
            shuffle(remain)
            orders += remain

            # find best pair for each order
            for order in orders[2:]:

                possible_value = param_values[order]
                best_param_value = -1
                best_pair_cross = -1

                for value in possible_value:
                    pair_cross = 0
                    for test in testset:
                        if unused_pair_search[value][test] or unused_pair_search[test][value]:
                            pair_cross += 1

                    if pair_cross > best_pair_cross:
                        best_pair_cross = pair_cross
                        best_param_value = value

                testset.append(best_param_value)

            # find coverage of this testset

            coverage = 0
            for i in testset:
                for j in testset:
                    if unused_pair_search[i][j]:
                        coverage += 1

            if coverage > best_testset_coverage:
                best_testset_coverage = coverage
                best_testset = testset

        # got best testset, kill some pair out
        for i in best_testset:
            for j in best_testset:
                if unused_pair_search[i][j]:
                    unused_pair_search[i][j] = 0
                    all_pairs_num -= 1

        # add to testsets
        testset_value = [all_values[i] for i in testset]
        testsets.append(testset_value)


    return {'params': param_names, 'tests': testsets}

def main():

    filename =  sys.argv[1]
    input_list = []
    with open(filename,"r") as f:
        for line in f:
            text = line.strip()
            if not text:
                continue
            param_name, param_values = text.split(":")
            param_name = param_name.strip()
            param_values = param_values.split()
            input_list.append((param_name,param_values))

    pairwised = pairwise(input_list)

    params = "\t".join(pairwised['params'])
    print params

    for test in pairwised["tests"]:
        teststr = "\t".join(test)
        print teststr

if __name__ == '__main__':
    main()