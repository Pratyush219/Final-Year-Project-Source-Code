import numpy as np
import heapq
from itertools import combinations, chain

class Rule:
    def __init__(self, itemset: set, left: set, right: set, supp, conf, lift) -> None:
        self.itemset = itemset
        self.left = left
        self.right = right
        self.conf = conf
        self.supp = supp
        self.lift = lift

    
def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def count_occurences(itemset, transactions):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count

def join_two_itemsets(it1, it2, order):
    it1.sort(key = lambda x: order.index(x.split(',')[0]))
    it2.sort(key = lambda x: order.index(x.split(',')[0]))

    for i in range(len(it1) - 1):
        if it1[i] != it2[i]:
            return []
    split_str1 = it1[-1].split(',')
    split_str2 = it2[-1].split(',')
    id1 = order.index(split_str1[0])
    id2 = order.index(split_str2[0])
    if id1 < id2:
        return it1 + [it2[-1]]
    return []

def join_set_itemsets(itemsets, order):
    C = []
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            item_out = join_two_itemsets(itemsets[i], itemsets[j], order)
            if len(item_out) > 0:
                C.append(item_out)
    return C


def calculate_confidence(left, itemset, transactions):
    supp_itemset = count_occurences(itemset, transactions)
    supp_left = count_occurences(left, transactions)
    return supp_itemset/supp_left
def get_frequent(itemsets, transactions, n_itemsets, order):
    # Store the support counts of all the itemsets
    support_counts_for_items = []
    for itemset in itemsets:
        support = count_occurences(itemset, transactions)
        if support > 0:
            support_counts_for_items.append((itemset, support))
    # heapq implements min-heap by default but we want a max-heap. In order to simulate that behaviour, we multiply the support counts with -1. The most negative value will be the minimum and will be at the top of the heap.
    counts = [-item[1] for item in support_counts_for_items]

    # heapify the counts list
    heapq.heapify(counts)
    # Stores the list of frequent itemsets along with their support
    frequent_itemsets_with_support = list() 
    # Stores the list of frequent itemsets
    frequent_itemsets = list()
    # Stores the list of support counts of frequent itemsets
    support = list()
    # A set that is used to track whether an itemset has already been added to frequent_itemsets
    added = set()
    num_itemsets_added = 0
    while num_itemsets_added < n_itemsets and len(counts) != 0:
        count = heapq.heappop(counts)
        # Iterate through all the itemsets
        for item, supp in support_counts_for_items:
            # If support of current itemset is equal to count and it has not been added to frequent_itemsets
            if supp == -count and str(item) not in added:
                frequent_itemsets_with_support.append([item, supp])
                added.add(str(item))
        num_itemsets_added += 1

    # Sort the itemsets in the correct order ot allow joining of itemsets
    frequent_itemsets_with_support.sort(key=lambda x: tuple(order.index(d.split(',')[0]) for d in x[0]))
    # First item of each entry is an itemset
    frequent_itemsets = [entry[0] for entry in frequent_itemsets_with_support]
    # Second item of each entry is support count
    support = [entry[1] for entry in frequent_itemsets_with_support]
    return frequent_itemsets, support

def get_confident_rules(L, frequent_itemsets, n_rules, transactions):
    #TODO: Generate confident rules based on the algorithm in the base paper
    rules = []
    itemsets_considered = []
    num_trans = len(transactions)
    for j in range(len(frequent_itemsets)):
        s = list(powerset(set(frequent_itemsets[j])))
        s.pop()
        curr_rules = []
        should_consider_this_itemset = True
        for z in s:
            S = set(z)
            X = set(frequent_itemsets[j])
            X_S = set(X - S)
            if len(S) > 0 and S in itemsets_considered:
                should_consider_this_itemset = False
                break
            sup_x = count_occurences(X, transactions)
            sup_x_s = count_occurences(X_S, transactions)
            conf = calculate_confidence(S, X, transactions)
            lift = sup_x/(sup_x_s/num_trans)
            curr_rules.append(Rule(X, S, X_S, sup_x, conf, lift))
        if should_consider_this_itemset:
            print(frequent_itemsets[j], "considered")
            rules += curr_rules
        else:
            print(frequent_itemsets[j], "not considered")
    rules.sort(key=lambda x: x.conf, reverse=True)
    print("Intermediate rules:")
    print(rules)
    return rules[:n_rules]

def generate_features(rules, columns):
    features = []
    for rule in rules:
        # Check if the consequent consists of exactly one item and that is a value corresponding to the Outcome field. If yes, then the antecedent is one of the features
        if len(rule[1]) == 1 and rule[1].pop().split(',')[0] == columns[-1]:
            features.append(rule[0])
    return (features)