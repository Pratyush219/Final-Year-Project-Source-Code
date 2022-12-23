import pandas as pd
import numpy as np

# Used to find floor of a number in a sorted list. 
# floor is defined as the largest number not less than the given key
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

# Uses the pandas module to load data
def load_data(path: str):
    data = pd.read_csv(path)
    data.dropna()
    return data

# This method is used to split the continuous values attributes in a finite number of intervals in order to assist in classification
def discretize_data(data: pd.DataFrame, k: int):
    # Created a copy of original data. Keep original data as it is for backup
    transformed_data = data.copy()
    size = len(transformed_data)
    # Split the elements such that the number of elements in each interval stays the same except probably in the last interval
    interval_size = size//k
    for col in transformed_data.columns[:-1]:
        # Sort the values in current column
        sorted_data = sorted([float(val) for val in transformed_data[col]])
        max_val = max(sorted_data)
        split_points = []
        # Use a set to ensure that one split point gets added to the split_points
        value_added = set()
        for i in range(0, size, interval_size):
            # If not alreaady present in value_added, add it
            if sorted_data[i] not in value_added:
                split_points.append(sorted_data[i])
                value_added.add(sorted_data[i])

        for pos, val in enumerate(transformed_data[col]):
            # Used try except for debuggind purpose. Consider removing it in the future.
            try:
                split_pos = floor(split_points, val)
                # print(split_pos)
                left = str(split_points[split_pos])
                # Upper limit is the split_points[split_pos + 1] if it exists, else it is equal to the maximum value in the current column
                right = str(split_points[split_pos + 1]) if split_pos < (len(split_points) - 1) else str(max_val)
                # Assign the corrsponding cell string of the form 'left,right'
                transformed_data.loc[pos, col] = ','.join([col, left, right])
            except Exception as e:
                print(e)
                print(pos, col, val, split_pos, len(split_points))
            # print(pos, col)
    return transformed_data
