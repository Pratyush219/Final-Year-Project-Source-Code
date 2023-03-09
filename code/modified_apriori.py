from modified_ap_utils import *
import numpy as np
import pandas as pd
import pprint
from load_and_preprocess_data import load_data, get_label_appended_data, discretize_data

path_to_data = '../data/diabetes.csv'
n_itemsets = 30
n_rules = 50

data = load_data(path_to_data)
order = [col for col in data.columns]
transformed_data = get_label_appended_data(data)
print(transformed_data.columns)
transactions = transformed_data.to_numpy()

C = {}
L = {}
itemset_size = 1
items = []
itemsSet = set()
for transaction in transactions:
    for item in transaction:
        itemsSet.add(item)
items = [[item] for item in itemsSet]
items.sort(key = lambda x: order.index(x[0].split(',')[0]))
C.update({itemset_size: items})

def print_table(T, supp_count):
    print('Itemset | Frequency')
    for k in range(len(T)):
        print(f'{T[k]} : {supp_count[k]}')
    print()
    print()

supp_count_L = {}
frequent, support = get_frequent(items, transactions, n_itemsets, order)
L.update({itemset_size: frequent})
supp_count_L.update({itemset_size: support})

k = itemset_size + 1
convergence = False
while convergence == False:
    C.update({k: join_set_itemsets(L[k - 1], order)})
    print(f'Table C{k}: \n')
    print(len(C[k]))
    print_table(C[k], [count_occurences(it, transactions) for it in C[k]])
    frequent, support = get_frequent(C[k], transactions, n_itemsets, order)
    L.update({k: frequent})
    supp_count_L.update({k: support})
    if len(L[k]) == 0:
        convergence = True
    else:
        print(f'Table L{k}: \n')
        print(len(L[k]))
        print_table(L[k], supp_count_L[k])
        pass
    k += 1

def write_rules(X, S, X_S, conf, supp, lift):
    out_rules = ''
    out_rules += f'Freq. Itemset: {X}\n'
    out_rules += f'\tRule: {S} -> {X_S}\n'
    out_rules += f'\tConf: {conf:2.3f} '
    out_rules += f'\tSupp: {(supp/num_trans):2.3f} '
    out_rules += f'\tLift: {lift:2.3f}\n'
    return out_rules


assoc_rules_str = ''
rules_list = []
num_trans = len(transactions)
confident_rules = get_confident_rules(L[len(L) - 1], 10, transactions)
for rule in confident_rules:
    rules_list.append([list(rule.left), list(rule.right)])
    assoc_rules_str += write_rules(rule.itemset, rule.left, rule.right, rule.conf, rule.supp, rule.lift)

print(assoc_rules_str)

# for rule in rules_list:
    # if len(rule[1]) == 1 and list(rule[1])[0].split(',')[0] == order[-1]:
        # print(rule)
print("Features:")
pprint.pprint(generate_features(rules_list, order, transformed_data.columns))