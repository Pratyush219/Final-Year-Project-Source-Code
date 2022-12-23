import pandas as pd
import numpy as np
import math

def getSupportCount(dataset, itemset):
    pass
def read_data(filename):
    data = pd.read_csv(filename)
    print(data['Outcome'])
    for d in data:
        print(d)
def main():
    read_data('../data/diabetes.csv')
main()