import unittest
import pandas as pd
import numpy as np

from src.function_evaluator import FunctionEvaluator
from src.utils.data_info_type import DataInfoType
from src.data_handler.data_handler import DataSetHandler

class TestFunctionEvaluator(unittest.TestCase):
    def setUp(self):
        # Create sample training data
        train_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 1.2, 1.3, 1.4],
            'y2': [2.1, 2.2, 2.3, 2.4],
            'y3': [3.1, 3.2, 3.3, 3.4],
            'y4': [4.1, 4.2, 4.3, 4.4]
        })

        # Create sample the fours ideal data
        the_chosen_fours = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y2': [1.15, 1.25, 1.35, 1.45],
            'y8': [2.15, 2.25, 2.35, 2.45],
            'y7': [3.15, 3.25, 3.35, 3.45],
            'y5': [4.15, 4.25, 4.35, 4.45]
        })

        self.m_test_evaluator_obj = FunctionEvaluator(train_data, the_chosen_fours)
    
    def test_initialization(self):
        self.assertIsInstance(self.m_test_evaluator_obj, FunctionEvaluator)
    
    def test_evaluate_function_1(self):
        test_data_sample = {
            'x': 1,
            'y': 1.11
        }

        result = self.m_test_evaluator_obj.evaluate(test_data_sample)
        self.assertEqual(result, True)

    def test_evaluate_function_2(self):
        test_data_sample = {
            'x': 2,
            'y': 10
        }

        result = self.m_test_evaluator_obj.evaluate(test_data_sample)
        self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()
