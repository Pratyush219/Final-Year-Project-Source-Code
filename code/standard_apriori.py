from ap_utils import *
import numpy as np
import pandas as pd
import pprint
from load_and_preprocess_data import load_data, get_label_appended_data, discretize_data

from itertools import combinations, chain

class Rule:
    def __init__(self, itemset: set, left: set, right: set, supp, conf, lift):
        self.itemset = list(itemset)
        self.left = list(left)
        self.right = list(right)
        self.conf = conf
        self.supp = supp
        self.lift = lift

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def write_rules(X, X_S, S, conf, supp, lift, num_trans):
    rule = [S, X_S]
    out_rules = ''
    out_rules += f'Freq. Itemset: {X}\n'
    out_rules += f'\tRule: {S} -> {X_S}\n'
    out_rules += f'\tConf: {conf:2.3f} '
    out_rules += f'\tSupp: {(supp/num_trans):2.3f} '
    out_rules += f'\tLift: {lift:2.3f}\n'
    return out_rules, rule
def print_table(T, supp_count):
    print('Itemset | Frequency')
    for k in range(len(T)):
        print(f'{T[k]} : {supp_count[k]}')
    print()
    print()
def standard_apriori_features(filename):
    path_to_data = '../data/' + filename
    min_support = 0.01
    min_confidence = 0.01

    data = load_data(path_to_data)
    class_labels = set(data[data.columns[-1]])
    order = [col for col in data.columns]
    transformed_data = get_label_appended_data(data)
    # print(class_labels)

    transactions = transformed_data.to_numpy()
    # print(transactions)
    # print(order)

    C = {}
    L = {}
    itemset_size = 1
    discarded = {itemset_size: []}
    items = []
    itemsSet = set()
    for transaction in transactions:
        for item in transaction:
            itemsSet.add(item)
    # print(itemsSet)
    items = [[item] for item in itemsSet]
    items.sort(key = lambda x: order.index(x[0].split(',')[0]))
    C.update({itemset_size: items})
    # pprint.pprint(C[1])

    

    # print(f'Table C1: \n')
    # print(len(C[1]))
    # print_table(C[1], [count_occurences(it, transactions) for it in C[1]])
    supp_count_L = {}
    f, sup, new_discarded = get_frequent(C[itemset_size], transactions, min_support, discarded)
    discarded.update({itemset_size: new_discarded})
    L.update({itemset_size: f})
    supp_count_L.update({itemset_size: sup})
    # print(f'Table L1: \n')
    # print(len(L[1]))
    # print_table(L[1], supp_count_L[1])

    # print_table(L[1], supp_count_L[1])
    # pprint.pprint(items)

    k = itemset_size + 1
    convergence = False
    while convergence == False:
        C.update({k: join_set_itemsets(L[k - 1], order)})
        # print(f'Table C{k}: \n')
        # print(len(C[k]))
        # print_table(C[k], [count_occurences(it, transactions) for it in C[k]])
        f, sup, new_discarded = get_frequent(C[k], transactions, min_support, discarded)
        discarded.update({k: new_discarded})
        L.update({k: f})
        supp_count_L.update({k: sup})
        if len(L[k]) == 0:
            convergence = True
        else:
            # print(f'Table L{k}: \n')
            # print(len(L[k]))
            # print_table(L[k], supp_count_L[k])
            pass
        k += 1

    # pprint.pprint(L[k - 2])


    # ## Generate Rules



    assoc_rules_str = ''
    rules_list = []
    num_trans = len(transactions)
    for i in range(1, len(L)):
        for j in range(len(L[i])):
            s = list(powerset(set(L[i][j])))
            s.pop()
            for z in s:
                S = set(z)
                X = set(L[i][j])
                X_S = set(X - S)
                if len(X_S) == 1:
                    # print(X_S)
                    sup_x = count_occurences(X, transactions)
                    sup_x_s = count_occurences(X_S, transactions)
                    conf = sup_x/count_occurences(S, transactions)
                    lift = sup_x/(sup_x_s/num_trans)
                    if conf >= min_confidence and sup_x >= min_support:
                        rule_output, rule = write_rules(X, X_S, S, conf, sup_x, lift, num_trans)
                        # print(rule_output)
                        assoc_rules_str += rule_output
                        # rules_list.append(Rule())
                        rules_list.append(Rule(X, S, X_S, sup_x, conf, lift))

    # print(assoc_rules_str)
    # print(len(assoc_rules_str.split('\n')))


    # print('Features:')
    features, lifts = generate_features(rules_list, order, class_labels)
    # pprint.pprint(features)
    # print(lifts)
    return features, lifts

# standard_apriori_features('../data/diabetes.csv')
# standard_apriori_features('diabetes.csv')