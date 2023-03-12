import pprint, heapq
import pandas as pd

def get_items_dict_and_items_support(data: pd.DataFrame):
    items = dict()
    for col in data.columns[:-1]:
        for item in data[col]:
            if item not in items:
                items[item] = 0
            items[item] -= 1
    transactions = dict()
    for i in range(len(data)):
        transactions[i] = dict.fromkeys(items, 0)
    for pos, row in enumerate(data.values):
        for value in row:
            transactions[pos][value] = 1
    return items, transactions
def get_support_count(transactions: dict, itemset):
    support_count = 0
    for transaction in transactions.values():
        contains_itemset = True
        for item in itemset:
            contains_itemset &= transaction[item]
        if contains_itemset:
            support_count -= 1
    return support_count

def get_confident_rules(data: pd.DataFrame):
    items, transactions = get_items_dict_and_items_support(data)
    # pprint.pprint(items)
    # pprint.pprint(transactions)
    counts = list(items.values())
    dfreq = 30
    heapq.heapify(counts)
    frequent_items = dict()
    for count in counts[:dfreq]:
        for k, v in items.items():
            if v == count and (k, v) not in frequent_items:
                frequent_items[k] = v
                
    