import numpy as np
import pandas as pd

class IdealFunctionSelector:
    def __init__(self, training_data, ideal_data):

        if training_data is None or ideal_data is None:
            raise ValueError("Training data and ideal data is None.")

        if training_data.empty or ideal_data.empty:
            raise ValueError("Training data and ideal data is empty.")

        self.m_training_data = training_data
        self.m_ideal_data = ideal_data
        self.m_the_fours_ideal = {}

    staticmethod
    def get_least_squared_list(self, train_col_idx):
        """
        Calculate the least squares deviation for a single training column 
        against all ideal columns and return the sorted deviations.
        """
        try:
            if train_col_idx not in self.m_training_data.columns:
                raise KeyError(f"Column '{train_col_idx}' not found in training data.")
            
            list_of_deviations = []
            
            for ideal_col_idx in self.m_ideal_data.columns[1:]:   # Discard 1st row which contains x data
                if ideal_col_idx not in self.m_ideal_data.columns:
                    raise KeyError(f"Ideal function column '{ideal_col_idx}' not found.")

                deviation = np.sum((self.m_training_data[train_col_idx] - self.m_ideal_data[ideal_col_idx]) ** 2)
                list_of_deviations.append((ideal_col_idx, deviation))

            return sorted(list_of_deviations, key=lambda x: x[1], reverse=False)

        except KeyError as ke:
            raise KeyError(f"Data column error: {ke}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in get_least_squared_list: {e}")

    def find_ideal_functions(self):
        """
        The criterion for choosing the ideal functions for the training function is how 
        they minimize the sum of all y-deviations squared (Least-Square)
        """
        try:
            for train_col_idx in self.m_training_data.columns[1:]:
                list_of_deviations = self.get_least_squared_list(train_col_idx)

                # Select the ideal function with the least deviation which is 1st item of sorted list of deviation
                self.m_the_fours_ideal[train_col_idx] = list_of_deviations[0]
            
            # Create a new DataFrame for the the fours ideal function
            result = pd.DataFrame()
            result['x'] = self.m_training_data['x']  # Copy the x column from train data

            for train_col, (ideal_func, deviation) in self.m_the_fours_ideal.items():
                result[ideal_func] = self.m_ideal_data[ideal_func]

            return result

        except KeyError as ke:
            raise KeyError(f"Data structure error: {ke}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in find_ideal_functions: {e}")