import pandas as pd
import numpy as np
FILENAME = '../data/diabetes.csv'
def floor(l: list, key):
    left = 0
    right = len(l) - 1
    while left <= right:
        mid = (left + right)//2
        if l[mid] > key:
            right = mid - 1
        elif l[mid] < key:
            left = mid + 1
        else:
            return mid
    return right

def load_data(path: str):
    data = pd.read_csv(path)
    return data
def discretize_data(data: pd.DataFrame, k: int):
    transformed_data = data.copy()
    size = len(transformed_data)
    interval_size = size//k
    for col in transformed_data.columns[:-1]:
        sorted_data = sorted([float(val) for val in transformed_data[col]])
        max_val = max(sorted_data)
        cut_points = []
        for i in range(0, size, interval_size):
            if sorted_data[i] not in cut_points:
                cut_points.append(sorted_data[i])
            
        print(col, cut_points)
        for pos, val in enumerate(transformed_data[col]):
            try:
                split_pos = floor(cut_points, val)
                # print(split_pos)
                left = str(cut_points[split_pos])
                right = str(cut_points[split_pos + 1]) if split_pos < (len(cut_points) - 1) else str(max_val)
                transformed_data.loc[pos, col] = ','.join([left ,right])
            except Exception as e:
                print(e)
                print(pos, col, val, split_pos, len(cut_points))
            # print(pos, col)
    return transformed_data
def main():
    data = load_data(FILENAME)
    data.dropna(inplace=True)
    num_intervals = 5
    # for col in data.columns[:-1]:
    #     data[col] = data[col].astype(float)
    transformed_data = discretize_data(data, num_intervals)
    print(transformed_data)
main()