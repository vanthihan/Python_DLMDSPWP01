import numpy as np
import pandas as pd

class TestDataEvaluator:
    def __init__(self, test_data, ideal_data, chosen_functions, training_data):
        self.test_data = test_data
        self.ideal_data = ideal_data
        self.chosen_functions = chosen_functions
        self.training_data = training_data

    def evaluate(self):
        results = []
        for _, row in self.test_data.iterrows():
            x, y = row['x'], row['y']
            for train_col, ideal_col in self.chosen_functions.items():
                ideal_y = self.ideal_data.loc[self.ideal_data['x'] == x, ideal_col].values
                if len(ideal_y) == 0:
                    continue
                ideal_y = ideal_y[0]
                deviation = abs(y - ideal_y)
                max_allowed_deviation = np.sqrt(2) * max(abs(self.training_data[train_col] - self.ideal_data[ideal_col]))
                if deviation <= max_allowed_deviation:
                    results.append({'x': x, 'y': y, 'ideal_function': ideal_col, 'deviation': deviation})
                    break
        return pd.DataFrame(results)