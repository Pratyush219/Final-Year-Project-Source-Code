from modified_ap_utils import *
import numpy as np
import pandas as pd
import pprint
from load_and_preprocess_data import load_data, get_label_appended_data, discretize_data

path_to_data = '../data/diabetes.csv'
n_itemsets = 30
n_rules = 15

data = discretize_data(load_data(path_to_data), 8)
order = [col for col in data.columns]
transformed_data = get_label_appended_data(data)
print(transformed_data.columns)
transactions = transformed_data.to_numpy()

C = {}
frequent_itemsets = {}
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
frequent_itemsets.update({itemset_size: frequent})
supp_count_L.update({itemset_size: support})

k = itemset_size + 1
convergence = False
while convergence == False:
    C.update({k: join_set_itemsets(frequent_itemsets[k - 1], order)})
    print(f'Table C{k}: \n')
    print(len(C[k]))
    print_table(C[k], [count_occurences(it, transactions) for it in C[k]])
    frequent, support = get_frequent(C[k], transactions, n_itemsets, order)
    frequent_itemsets.update({k: frequent})
    supp_count_L.update({k: support})
    if len(frequent_itemsets[k]) == 0:
        convergence = True
    else:
        print(f'Table L{k}: \n')
        print(len(frequent_itemsets[k]))
        print_table(frequent_itemsets[k], supp_count_L[k])
        pass
    k += 1

all_frequent_itemsets = []
for size, itemsets in frequent_itemsets.items():
    if size > 1:
        all_frequent_itemsets += itemsets

required_frequent_itemsets, support = get_frequent(all_frequent_itemsets, transactions, n_itemsets, order)
pprint.pprint(required_frequent_itemsets)
def write_rules(X, S, X_S, conf, rconf, supp, lift):
    out_rules = ''
    out_rules += f'Freq. Itemset: {X}\n'
    out_rules += f'\tRule: {S} -> {X_S}\n'
    out_rules += f'\tConf: {conf:2.3f} '
    out_rules += f'\trConf: {rconf:2.3f}\n'
    out_rules += f'\tSupp: {(supp/num_trans):2.3f} '
    out_rules += f'\tLift: {lift:2.3f}\n'
    return out_rules


assoc_rules_str = ''
rules_list = []
num_trans = len(transactions)
confident_rules = get_confident_rules(frequent_itemsets, required_frequent_itemsets, n_rules, transactions)
for rule in confident_rules:
    rules_list.append([list(rule.left), list(rule.right)])
    assoc_rules_str += write_rules(rule.itemset, rule.left, rule.right, rule.conf, rule.rconf, rule.supp, rule.lift)

print(assoc_rules_str)

print("Features:")
pprint.pprint(generate_features(rules_list, transformed_data.columns))