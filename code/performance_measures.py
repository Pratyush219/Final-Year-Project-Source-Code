import math
from standard_apriori import standard_apriori_features
from modified_apriori import modified_apriori_features

filename = '../data/heart_2020_cleaned.csv'

def performance_measures(results1, results2, std_apr_lifts, modified_apr_lifts):
    std_apr_lifts_len = len(std_apr_lifts)
    if std_apr_lifts_len == 0:
        mean_std = 0
    else:
        mean_std= sum(std_apr_lifts)/std_apr_lifts_len

    modified_apr_lifts_len = len(modified_apr_lifts)
    if modified_apr_lifts_len == 0:
        mean_modified = 0
    else:
        mean_modified = sum(modified_apr_lifts)/modified_apr_lifts_len

    std_apr_lifts.sort()
    median_std = 0
    if std_apr_lifts_len % 2 == 1:
        median_std = std_apr_lifts[std_apr_lifts_len//2]
    elif std_apr_lifts_len > 0:
        median_std = (std_apr_lifts[std_apr_lifts_len//2] + std_apr_lifts[(std_apr_lifts_len//2)-1])/2

    modified_apr_lifts.sort()
    median_modified = 0
    if modified_apr_lifts_len % 2 == 1:
        median_modified = modified_apr_lifts[modified_apr_lifts_len//2]
    elif modified_apr_lifts_len > 0:
        median_modified = (modified_apr_lifts[modified_apr_lifts_len//2] + modified_apr_lifts[(modified_apr_lifts_len//2)-1])/2

    std_variance = 0
    if std_apr_lifts_len == 1:
        std_variance = 0
    else:
        local_list = []
        for items in std_apr_lifts:
            local_list.append((items-mean_std)**2)
        std_variance = sum(local_list) / (std_apr_lifts_len-1)

    mod_variance = 0
    if modified_apr_lifts_len == 1:
        mod_variance = 0
    else:
        local_list = []
        for items in modified_apr_lifts:
            local_list.append((items-mean_modified)**2)
        mod_variance = sum(local_list) / (modified_apr_lifts_len-1)

    std_standard_deviation = math.sqrt(std_variance)
    mod_standard_deviation = math.sqrt(mod_variance)

    print(mean_std, mean_modified, median_std, median_modified, std_variance, mod_variance, std_standard_deviation, mod_standard_deviation) 

result1, lifts1 = standard_apriori_features(filename)

print("Standarad Apriori Done")

result2, lifts2 = modified_apriori_features(filename)
performance_measures(result1, result2, lifts1, lifts2)

