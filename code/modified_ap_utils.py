import numpy as np
import heapq
from itertools import combinations, chain

support_counts = dict()
class Rule:
    def __init__(self, itemset: set, left: set, right: set, supp, conf, lift, rconf) -> None:
        self.itemset = list(itemset)
        self.left = list(left)
        self.right = list(right)
        self.conf = conf
        self.supp = supp
        self.lift = lift
        self.rconf = rconf
        
        # print('-------------------------------------------')
        # print(self.left,"->",self.right)
        # print("rconf: ",rconf," conf: ",conf)    
        # print('-------------------------------------------')    

def ordered_itemset(itemset, order):
    return sorted(list(itemset), key = lambda x: order.index(x.split(",")[0]))
def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def count_occurences(itemset, transactions):
    if itemset in support_counts:
        return support_counts[itemset]
    count = 0
    for transaction in transactions:
        if itemset.issubset(set(transaction)):
            count += 1
    support_counts[itemset] = count
    return count

def join_two_itemsets(it1: frozenset, it2: frozenset, order):
    combinedItemset = it1.union(it2)
    labels1 = set([item.split(',')[0] for item in it1])
    labels2 = set([item.split(',')[0] for item in it2])

    labelsCombined = labels1.union(labels2)
    if len(combinedItemset) == len(labelsCombined) == 1 + len(it1):
        return combinedItemset
    return frozenset()

def join_set_itemsets(itemsets, k, order):
    C = []
    itemsetsToBeJoined = []
    for itemset in itemsets:
        if len(itemset) == k:
            itemsetsToBeJoined.append(itemset)
    for i in range(len(itemsetsToBeJoined)):
        for j in range(i + 1, len(itemsetsToBeJoined)):
            item_out = join_two_itemsets(itemsetsToBeJoined[i], itemsetsToBeJoined[j], order)
            if len(item_out) > 0:
                C.append(item_out)
    return C


def calculate_confidence(left, itemset, transactions):
    supp_itemset = count_occurences(itemset, transactions)
    supp_left = count_occurences(left, transactions)
    return supp_itemset/supp_left

def calculate_rel_confidence(left, right,  itemset, transactions):
    supp_itemset = count_occurences(itemset, transactions)
    supp_left = count_occurences(left, transactions)
    supp_right = count_occurences(right, transactions)
    if supp_left - supp_itemset == 0:
        return float('inf')
    rconf = (supp_itemset/(supp_left-supp_itemset))*((len(transactions)-supp_right)/supp_right)
    return rconf

# def get_frequent(itemsets, transactions, n_itemsets, order):
#     # Store the support counts of all the itemsets
#     #support_counts_for_items = []
#     support_counts_for_items = {}
#     for itemset in itemsets:
#         class_label = ordered_itemset(itemset, order)[-1]

#         # if class_label not in ['class,tested_negative', 'class,tested_positive']:
#         #     raise Exception("Different class label: ", class_label)
        
#         support = count_occurences(itemset, transactions)
#         if class_label not in support_counts_for_items.keys():
#             support_counts_for_items[class_label]=[]
#         if support > 0:
#             support_counts_for_items[class_label].append((itemset, support))
#     # print("Number of class labels: ", len(support_counts_for_items))
#     # Stores the list of frequent itemsets along with their support
#     frequent_itemsets_with_support = list() 
#     # Stores the list of frequent itemsets
#     frequent_itemsets = list()
#     # Stores the list of support counts of frequent itemsets
#     support = list()

#     itemsets_per_class = int(n_itemsets/len(support_counts_for_items))
#     for (key, value) in support_counts_for_items.items():
#         frequent_itemsets_with_support += sorted(list(value), key=lambda x: x[1], reverse=True)[:itemsets_per_class]
#     # Sort the itemsets in the correct order ot allow joining of itemsets
#     frequent_itemsets_with_support.sort(key=lambda x: tuple(order.index(d.split(',')[0]) for d in x[0]))
#     # First item of each entry is an itemset
#     frequent_itemsets = [entry[0] for entry in frequent_itemsets_with_support]
#     # Second item of each entry is support count
#     support = [entry[1] for entry in frequent_itemsets_with_support]
#     return frequent_itemsets, support

# def get_confident_rules(frequent_itemsets, n_rules, transactions, order):
#     class_label = order[-1]
#     rules = []
#     num_trans = len(transactions)
#     for j in range(len(frequent_itemsets)):
#         s = list(powerset(frequent_itemsets[j]))
#         s.pop()
#         curr_rules = []
#         for z in s:
#             S = frozenset(z)
#             X = frequent_itemsets[j]
#             X_S = frozenset(X - S)
#             if len(X_S) == 1 and list(X_S)[0].split(',')[0] == class_label:
#                 sup_x = count_occurences(X, transactions)
#                 sup_x_s = count_occurences(X_S, transactions)
#                 conf = calculate_confidence(S, X, transactions)
#                 rconf = calculate_rel_confidence(S, X_S, X, transactions)
#                 lift = sup_x/(sup_x_s/num_trans)
#                 temp_rule = Rule(
#                                 ordered_itemset(X, order), 
#                                 ordered_itemset(S, order), 
#                                 ordered_itemset(X_S, order), 
#                                 sup_x, conf, lift, rconf)
#                 if reduce_redundancy(temp_rule,transactions):
#                     curr_rules.append(temp_rule)
#         rules += curr_rules
#     rules.sort(key=lambda x: x.rconf, reverse=True)
#     # print("Intermediate rules:")
#     # print(rules)
#     return rules[:n_rules]


def get_frequent(itemsets, transactions, n_itemsets, order, class_labels):
    # Store the support counts of all the itemsets
    #support_counts_for_items = []
    support_counts_for_items = {}
    for itemset in itemsets:
        class_label = ordered_itemset(itemset, order)[-1]

        # if class_label not in ['class,tested_negative', 'class,tested_positive']:
        #     raise Exception("Different class label: ", class_label)
        
        support = count_occurences(itemset, transactions)
        if class_label not in support_counts_for_items.keys():
            support_counts_for_items[class_label]=[]
        if support > 0:
            support_counts_for_items[class_label].append((itemset, support))
    # print("Number of class labels: ", len(support_counts_for_items))
    # Stores the list of frequent itemsets along with their support
    frequent_itemsets_with_support = list() 
    # Stores the list of frequent itemsets
    frequent_itemsets = list()
    # Stores the list of support counts of frequent itemsets
    support = list()

    itemsets_per_class = int(n_itemsets/len(class_labels))
    for (key, value) in support_counts_for_items.items():
        frequent_itemsets_with_support += sorted(list(value), key=lambda x: x[1], reverse=True)[:itemsets_per_class]
    # Sort the itemsets in the correct order ot allow joining of itemsets
    frequent_itemsets_with_support.sort(key=lambda x: tuple(order.index(d.split(',')[0]) for d in x[0]))
    # First item of each entry is an itemset
    frequent_itemsets = [entry[0] for entry in frequent_itemsets_with_support]
    # Second item of each entry is support count
    support = [entry[1] for entry in frequent_itemsets_with_support]
    return frequent_itemsets, support

def get_confident_rules(frequent_itemsets, n_rules, transactions, order):
    class_label = order[-1]
    rules = []
    num_trans = len(transactions)
    for j in range(len(frequent_itemsets)):
        s = list(powerset(frequent_itemsets[j]))
        s.pop()
        curr_rules = []
        for z in s:
            S = frozenset(z)
            X = frequent_itemsets[j]
            X_S = frozenset(X - S)
            if len(X_S) == 1 and list(X_S)[0].split(',')[0] == class_label:
                sup_x = count_occurences(X, transactions)
                sup_x_s = count_occurences(X_S, transactions)
                conf = calculate_confidence(S, X, transactions)
                rconf = calculate_rel_confidence(S, X_S, X, transactions)
                lift = sup_x/(sup_x_s/num_trans)
                temp_rule = Rule(
                                ordered_itemset(X, order), 
                                ordered_itemset(S, order), 
                                ordered_itemset(X_S, order), 
                                sup_x, conf, lift, rconf)
                if reduce_redundancy(temp_rule,transactions):
                    curr_rules.append(temp_rule)
        rules += curr_rules
    rules.sort(key=lambda x: x.rconf, reverse=True)
    # print("Intermediate rules:")
    # print(rules)
    return rules[:n_rules]


conf_rules_right = {}
final_features = {}
def generate_features(rules, columns, class_labels):
    features_dict = {}
    lifts = []
    for class_label in class_labels:
        features_dict[str(class_label)] = set()
        conf_rules_right[str(class_label)] = []
    print(features_dict)
    print(conf_rules_right)
    for rule in rules:
        # Check if the consequent consists of exactly one item and that is a value corresponding to the Outcome field. If yes, then the antecedent is one of the features
        cell = ordered_itemset(rule.right, columns)[-1].split(',')
        if len(rule.right) == 1 and cell[0] == columns[-1]:
            # features.append(rule[0])
            label = cell[1]
            if label not in features_dict:
                features_dict[label] = set()
                conf_rules_right[label] = []
            features_dict[label].add(tuple(rule.left))
            lifts.append(rule.lift)
            conf_rules_right[label].append([rule.left,rule.rconf])

    for key in conf_rules_right:
        final_features[key] = set()
        for items in conf_rules_right[key]:
            # print('=======ITEMS=======',items)
            left = items[0]
            rconf = items[1]
            for check_items in conf_rules_right[key]:
                # print('=======CHECK_ITEMS=======',check_items)
                check_items_left = check_items[0]
                check_items_rconf = check_items[1]
                if left[0] in check_items_left:
                    if rconf > check_items_rconf:
                        # final_features[key].add(tuple(left))
                        continue
                    elif rconf < check_items_rconf:
                        # final_features[key].add(tuple(check_items_left))
                        left = check_items_left
                        rconf = check_items_rconf
            final_features[key].add(tuple(left))
    return (features_dict ,final_features, lifts)

def reduce_redundancy(rule, transactions):
    left = frozenset(rule.left)
    right = frozenset(rule.right) 
    itemset = frozenset(rule.itemset)
    rel_conf_itemset = calculate_rel_confidence(left,right,itemset,transactions)
    verdict = False
    if(len(rule.left) > 1):
        flag = True
        for i in left:
            i = frozenset(list(i))
            flag &= (calculate_rel_confidence(i,right,itemset,transactions) <= rel_conf_itemset)
        if flag:
            verdict = True
    else:
        verdict = True
    return verdict