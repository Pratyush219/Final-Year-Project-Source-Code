import load_and_preprocess_data as load
FILENAME = '../data/diabetes.csv'
data = load.load_data(FILENAME)
transformed_data = load.discretize_data(data, 5)
print(transformed_data)