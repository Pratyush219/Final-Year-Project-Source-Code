import load_and_preprocess_data as load
FILENAME = '../data/diabetes.csv'

data = load.load_data(FILENAME)
transformed_data = load.discretize_data(data, 5)
# gen.get_confident_rules(transformed_data)
print(transformed_data)