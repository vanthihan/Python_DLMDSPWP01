import unittest
import pandas as pd
import numpy as np
from src.ideal_function_selector import IdealFunctionSelector

class TestIdealFunctionSelector(unittest.TestCase):
    def setUp(self):
        # Create sample training data
        self.training_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 1.2, 1.3, 1.4],
            'y2': [2.1, 2.2, 2.3, 2.4],
            'y3': [3.1, 3.2, 3.3, 3.4],
            'y4': [4.1, 4.2, 4.3, 4.4]
        })
        
        # Create sample ideal data
        self.ideal_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [11.15, 12.15, 13.1, 14.1],
            'y2': [1.15, 1.25, 1.35, 1.45],     # Expect to match with training_y1
            'y3': [21.15, 22.15, 23.15, 24.15],
            'y4': [31.15, 32.15, 33.15, 34.15],
            'y5': [4.15, 4.25, 4.35, 4.45],     # Expect to match with training_y4
            'y6': [51.15, 52.15, 53.15, 54.15],
            'y7': [3.15, 3.25, 3.35, 3.45],     # Expect to match with training_y3
            'y8': [2.15, 2.25, 2.35, 2.45],     # Expect to match with training_y2
        })
        
        self.m_selector_obj = IdealFunctionSelector(self.training_data, self.ideal_data)
    
    def test_initialization(self):
        self.assertIsInstance(self.m_selector_obj, IdealFunctionSelector)
    
    def test_find_ideal_functions(self):
        expected_best_4_funcs = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y2': [1.15, 1.25, 1.35, 1.45],
            'y8': [2.15, 2.25, 2.35, 2.45],
            'y7': [3.15, 3.25, 3.35, 3.45],
            'y5': [4.15, 4.25, 4.35, 4.45]
        })

        result = self.m_selector_obj.find_ideal_functions()
        pd.testing.assert_frame_equal(expected_best_4_funcs, result)

if __name__ == "__main__":
    unittest.main()
