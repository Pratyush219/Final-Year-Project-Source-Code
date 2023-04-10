from modified_ap_utils import *
import pprint
from load_and_preprocess_data import load_data, get_label_appended_data, discretize_data

path_to_data = '../data/diabetes1.csv'
n_itemsets = 30
n_rules = 15

data = load_data(path_to_data)
print('Data loaded')
order = [col for col in data.columns]
transformed_data = get_label_appended_data(data)
print(transformed_data)
print('data transformed')
#print(transformed_data.columns)
transactions = transformed_data.to_numpy()
print(transactions)

candidates = {}
frequent_itemsets = {}
itemset_size = 1
items = []
itemsSet = set()
for transaction in transactions:
    for item in transaction[:-1]:
        itemsSet.add(frozenset([item, transaction[-1]]))
items = [item for item in itemsSet]
items.sort(key = lambda x: order.index(list(x)[0].split(',')[0]))
candidates.update({itemset_size: items})

def print_table(T, supp_count):
    print('Itemset | Frequency')
    for k in range(len(T)):
        print(f'{ordered_itemset(T[k], order)} : {supp_count[k]}')
    print()
    print()

supp_count_L = {}
frequent, support = get_frequent(candidates[itemset_size], transactions, n_itemsets, order)
frequent_itemsets.update({itemset_size: frequent})
supp_count_L.update({itemset_size: support})

k = itemset_size + 1
convergence = False
while convergence == False:
    candidates.update({k: join_set_itemsets(frequent_itemsets[k - 1], k, order)})
    if len(candidates[k]) > 0:
        candidates[k] += candidates[k - 1]
        print(f'Table C{k}: \n')
        print(len(candidates[k]))
        print_table(candidates[k], [count_occurences(it, transactions) for it in candidates[k]])
        frequent, support = get_frequent(candidates[k], transactions, n_itemsets, order)
        frequent_itemsets.update({k: frequent})
        supp_count_L.update({k: support})
    # Stop proceeding further if no candidates of size k are generated
    if len(candidates[k]) == 0:
        convergence = True
    else:
        print(f'Table L{k}: \n')
        print(len(frequent_itemsets[k]))
        print_table(frequent_itemsets[k], supp_count_L[k])
        k += 1
        if k == len(transactions[0]) - 1:
            convergence = True

print("Final itemsets:")
pprint.pprint(frequent_itemsets[k - 1])
def write_rules(rule: Rule):
    out_rules = ''
    out_rules += f'Freq. Itemset: {rule.itemset}\n'
    out_rules += f'\tRule: {rule.left} -> {rule.right}\n'
    out_rules += f'\tConf: {rule.conf:2.3f} '
    out_rules += f'\tSupp: {(rule.supp/num_trans):2.3f} '
    out_rules += f'\tLift: {rule.lift:2.3f}\n'
    return out_rules


assoc_rules_str = ''
rules_list = []
num_trans = len(transactions)
confident_rules = get_confident_rules(frequent_itemsets[k - 1], n_rules, transactions, order)
for rule in confident_rules:
    rules_list.append([list(rule.left), list(rule.right)])
    assoc_rules_str += write_rules(rule)

print(assoc_rules_str)

print("Features:")
pprint.pprint(generate_features(rules_list, transformed_data.columns))