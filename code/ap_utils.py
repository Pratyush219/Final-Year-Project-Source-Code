import numpy as np
import heapq
import pprint
def load_transactions(path_to_data, order):
    transactions = []
    with open(path_to_data, 'r') as fid:
        for lines in fid:
            str_line = list(lines.strip().split(','))
            _t = list(np.unique(str_line))
            _t.sort(key = lambda x: order.index(x))
            transactions.append(_t)
    return transactions

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

def get_frequent(itemsets, transactions, min_support, prev_discarded):
    L = []
    supp_count = []
    new_discarded = []
    k = len(prev_discarded)
    for itemset in itemsets:
        discarded_before = False
        if k > 0:
            for item in prev_discarded[k]:
                if set(item).issubset(set(itemset)):
                    discarded_before = True
                    break
        if not discarded_before:
            count = count_occurences(itemset, transactions)
            if count/len(transactions) >= min_support:
                L.append(itemset)
                supp_count.append(count)
            else:
                new_discarded.append(itemset)
    return L, supp_count, new_discarded

def modified_get_frequent(itemsets, transactions, n_itemsets, order):
    support_counts_for_items = [(itemset, count_occurences(itemset, transactions)) for itemset in itemsets]
    counts = [-item[1] for item in support_counts_for_items]
    support_counts_for_items.sort(key=lambda x: x[1], reverse=True)
    heapq.heapify(counts)
    # pprint.pprint(support_counts_for_items)
    # print(counts)
    frequent_itemsets = list()
    frequent = list()
    support = list()
    added = set()
    pops = 0
    while pops < n_itemsets and len(counts) != 0:
        count = heapq.heappop(counts)
        pops += 1
        for item, supp in support_counts_for_items:
            if supp == -count and not set(item).issubset(added):
                frequent_itemsets.append([item, supp])
                added.add(item[0])

    frequent_itemsets.sort(key=lambda x: tuple(order.index(d.split(',')[0]) for d in x[0]))
    # print(frequent_itemsets)
    frequent = [entry[0] for entry in frequent_itemsets]
    support = [entry[1] for entry in frequent_itemsets]
    # print(frequent)
    # print(support)
    return frequent, support
def get_confident_rules(itemsets, supp_count):
    pass
def generate_features(rules, order):
    features = []
    for rule in rules:
        if len(rule[1]) == 1 and rule[1].pop().split(',')[0] == 'Outcome':
            features.append(rule[0])
    return (features)