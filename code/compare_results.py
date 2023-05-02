import matplotlib.pyplot as plt
from standard_apriori import standard_apriori_features
from modified_apriori import modified_apriori_features
import time

filename = 'heart.csv'
# start_time = time.time()
# result1, lifts1 = standard_apriori_features(filename)
# end_time1 = time.time()
# print(result1)
# start_time2 = time.time()
unreduced_features, reduced_features, lifts2 = modified_apriori_features(filename)
# end_time2 = time.time()
# print(result2)

# print('Result1: ', result1)
# print('Result2: ', reduced_features)

# # calculate the runtime of each function
# runtime1 = end_time1 - start_time
# runtime2 = end_time2 - start_time2

# # create a bar graph to compare the runtimes
# functions = ['Standard Apriori', 'Modified Apriori']
# runtimes = [runtime1, runtime2]

# plt.figure()
# plt.bar(functions, runtimes)
# plt.title('Comparison of Function Runtimes')
# plt.xlabel('Functions')
# plt.ylabel('Runtime (s)')

# plt.savefig('runtime.jpg')

count_length_unreduced = []
for keys in unreduced_features:
    count_length_unreduced.append(len(unreduced_features[keys]))

class_label = []
count_length_reduced = []
for keys in reduced_features:
    class_label.append(str(keys))
    count_length_reduced.append(len(reduced_features[keys]))
print(class_label)
x_values1 = []
x_values2 = []
for i in range(len(class_label)):
    x_values1.append(i+1)
    x_values2.append(i+1+len(class_label))

plt.figure()
plt.bar(x_values1, count_length_unreduced, color='red')
plt.bar(x_values2, count_length_reduced, color='green')
plt.xlabel('Linear Spacing')
plt.ylabel('Number of features')
plt.title('Dataset length is 700')
plt.savefig('features.jpg')

# Add text labels to the bars
for i in range(len(x_values1)):
    plt.text(x=x_values1[i], y=count_length_unreduced[i], s=class_label[i], ha='center')

for i in range(len(x_values2)):
    plt.text(x=x_values2[i], y=count_length_reduced[i], s=class_label[i], ha='center', va='top')

# plt.savefig('my_plot.png')
# plt.show()
