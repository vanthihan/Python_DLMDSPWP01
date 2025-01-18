import pandas as pd
import time


def find_best_ideal_function(training_data, ideal_data):
    results = {}
    for col in training_data.columns[1:]:  # Skip 'x', iterate over 'y1', 'y2', etc.
        min_deviation = float('inf')
        best_function = None
        
        for ideal_col in ideal_data.columns[1:]:  # Skip 'x', iterate over 'y1', 'y2', ..., 'y50'
            deviation = ((training_data[col] - ideal_data[ideal_col])**2).sum()
            
            if deviation < min_deviation:
                min_deviation = deviation
                best_function = ideal_col
        
        results[col] = best_function
    return results

# Load data
training_data = pd.read_csv('./DataBase/dataset_1/train.csv')
ideal_data = pd.read_csv('./DataBase/dataset_1/ideal.csv')

# Measure execution time
start_time = time.time()
# Find best matches
best_matches = find_best_ideal_function(training_data, ideal_data)
end_time = time.time()

# Display results
print("Best matches:")
for train_func, ideal_func in best_matches.items():
    print(f"{train_func} -> {ideal_func}")

print(f"Execution Time: {end_time - start_time:.2f} seconds")

