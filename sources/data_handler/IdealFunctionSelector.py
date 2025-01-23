import numpy as np
import pandas as pd

class IdealFunctionSelector:
    def __init__(self, training_data, ideal_data):
        self.training_data = training_data
        self.ideal_data = ideal_data

    staticmethod
    def calculate_least_squares(self, train_col_idx):
        """
        Calculate the least squares deviation for a single training column 
        against all ideal columns and return the sorted deviations.
        """
        list_of_deviations = []
        
        for ideal_col_idx in self.ideal_data.columns[1:]:   # Discard 1st row which contains x data
            # Sum of all y-deviations squared (Least-Square)
            deviation = np.sum((self.training_data[train_col_idx] - self.ideal_data[ideal_col_idx]) ** 2)
            list_of_deviations.append((ideal_col_idx, deviation))

        # Sort the list ascendingly
        sorted_list_desc = sorted(list_of_deviations, key=lambda x: x[1], reverse=False)

        # Print out sorted list of deviation for debug
        # for ideal_func_index, deviation_val in sorted_list_desc:
        #     print(f"Train[{train_col_idx}]->Ideal[{ideal_func_index}]: Deviation Value = [{deviation_val:.5f}]")

        return sorted_list_desc

    def select_ideal_functions(self):
        """
        Map each training column to the ideal column with the least deviation 
        and return the transformed DataFrame.
        """
        selected_func_from_ideal = {}

        # Iterate over each training column (excluding the x column)
        for train_col_idx in self.training_data.columns[1:]:
            list_of_deviations = self.calculate_least_squares(train_col_idx)

            # Select the ideal function with the least deviation which is 1st item of sorted list of deviation
            selected_func_from_ideal[train_col_idx] = list_of_deviations[0]
        
        for train_func, (selected_ideal_func, deviation) in selected_func_from_ideal.items():
            print(f"Train function: [{train_func}] mapped to Ideal function: [{selected_ideal_func}] with deviation: [{deviation:.10f}]")

        # Create a new DataFrame for the result
        result = pd.DataFrame()
        result['x'] = self.training_data['x']  # Copy the x column

        # # Replace each training column with the corresponding ideal function's values
        for train_col, (selected_ideal_func, deviation) in selected_func_from_ideal.items():
            result[f"train[{train_col}]->ideal[{selected_ideal_func}]"] = self.ideal_data[selected_ideal_func]

        return result
