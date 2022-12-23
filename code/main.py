import continuous_to_categorical as cat
FILENAME = '../data/diabetes.csv'
data = cat.load_data(FILENAME)
transformed_data = cat.discretize_data(data, 5)
print(transformed_data)