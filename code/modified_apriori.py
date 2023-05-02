from modified_ap_utils import *
import pprint
import sys
import json
import math
from load_and_preprocess_data import load_data, get_label_appended_data, discretize_data
import matplotlib.pyplot as plt

def print_table(T, supp_count, order):
    print('Itemset | Frequency')
    for k in range(len(T)):
        print(f'{ordered_itemset(T[k], order)} : {supp_count[k]}')
    print()
    print()
    
def write_rules(rule: Rule, num_trans):
    out_rules = ''
    out_rules += f'Freq. Itemset: {rule.itemset}\n'
    out_rules += f'\tRule: {rule.left} -> {rule.right}\n'
    out_rules += f'\tConf: {rule.conf:2.3f} '
    out_rules += f'\trConf: {rule.rconf:2.3f}\n'
    out_rules += f'\tSupp: {(rule.supp/num_trans):2.3f} '
    out_rules += f'\tLift: {rule.lift:2.3f}\n'
    return out_rules
def modified_apriori_features(filename):
    path_to_data = '../data/' + filename

    n_itemsets = 150
    n_rules = 150
    n_record = 0
    data = load_data(path_to_data)
    data = discretize_data(data, 8)
    n_record = len(data)
    # print('Data loaded')
    order = [col for col in data.columns]
    class_labels = set(data[data.columns[-1]])
    # print(class_labels)
    transformed_data = get_label_appended_data(data)
    transactions = transformed_data.to_numpy()
    # print(transactions)

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

    

    supp_count_L = {}
    frequent, support = get_frequent(candidates[itemset_size], transactions, n_itemsets, order, class_labels)
    frequent_itemsets.update({itemset_size: frequent})
    supp_count_L.update({itemset_size: support})

    k = itemset_size + 1
    convergence = False
    while convergence == False:
        candidates.update({k: join_set_itemsets(frequent_itemsets[k - 1], k, order)})
        if len(candidates[k]) > 0:
            candidates[k] += candidates[k - 1]
            frequent, support = get_frequent(candidates[k], transactions, n_itemsets, order, class_labels)
            frequent_itemsets.update({k: frequent})
            supp_count_L.update({k: support})
        # Stop proceeding further if no candidates of size k are generated
        if len(candidates[k]) == 0:
            convergence = True
        else:
            k += 1
            if k == len(transactions[0]) - 1:
                convergence = True


    assoc_rules_str = ''
    rules_list = []
    num_trans = len(transactions)
    confident_rules = get_confident_rules(frequent_itemsets[k - 1], n_rules, transactions, order)

    for rule in confident_rules:
        rules_list.append([list(rule.left), list(rule.right)])
        assoc_rules_str += write_rules(rule, num_trans)

    # print(assoc_rules_str)

    (features_dict, final_features, lifts) = generate_features(confident_rules, order, class_labels)

    input_string = str(final_features)

    # Replace single quotes with double quotes
    input_string = input_string.replace("'", '"')
    # Evaluate the string as a Python dictionary
    input_dict = eval(input_string)
    # Convert the set objects into list objects
    for key in input_dict:
        input_dict[key] = [list(item) for item in input_dict[key]]
    # Convert the dictionary into a JSON object
    json_object = json.dumps(input_dict)

    # Print the JSON object as a string
    pprint.pprint(json_object)
    return features_dict, final_features, lifts

if __name__ == '__main__':
    modified_apriori_features(sys.argv[1])