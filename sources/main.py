from bokeh.layouts import row
from bokeh.plotting import figure, show
import pandas as pd

from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataSetHandler import TestDataSetHandler
from utils.exception import DataSetHandlerException

class TaskProcessor:
    def __init__(self, input_path, output_path):
        self.m_input_path = input_path
        self.m_output_path = output_path
        self.m_train_data_obj = None
        self.m_ideal_data_obj = None
        self.m_test_data_obj = None
        self.m_chosen_fours_data = None

    def data_init(self):
        csv_path_train = self.m_input_path + 'train.csv'
        csv_path_ideal = self.m_input_path + 'ideal.csv'
        csv_path_test = self.m_input_path + 'test.csv'

        sql_db_path_train = self.m_input_path + 'train.db'
        sql_db_path_ideal = self.m_input_path + 'ideal.db'
        sql_db_path_test = self.m_input_path + 'test.db'

        self.m_train_data_obj = DataSetHandler(csv_path_train, sql_db_path_train, 'train_db')
        self.m_ideal_data_obj = DataSetHandler(csv_path_ideal, sql_db_path_ideal, 'ideal_db')
        self.m_test_data_obj = TestDataSetHandler(csv_path_test, sql_db_path_test, 'test_db')

        self.m_train_data_obj.data_init()
        self.m_ideal_data_obj.data_init()
        self.m_test_data_obj.data_init()

    def find_ideal_functions(self):
        # Get SQLite data from initialized databases
        training_data = self.m_train_data_obj.load_from_db('train_db')
        ideal_data = self.m_ideal_data_obj.load_from_db('ideal_db')
        print(training_data, ideal_data)

        # Select ideal functions
        ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
        self.m_chosen_fours_data = ideal_func_selector_obj.select_ideal_functions()
        print(self.m_chosen_fours_data)

    def test_data_evaluation(self):
        test_data = self.m_test_data_obj.load_from_db('test_db')
        print(test_data)

    def plot_chosen_ideal_funcs(self) :
        # Create new datset hander object for best fit ideal functions
        chosen_fours_csv_path = output_path + 'best_4.csv'
        chosen_fours_sql_path = output_path + 'best_4.db'

        self.m_chosen_fours_data.to_csv(chosen_fours_csv_path, index=False)
        chosen_fours_obj = DataSetHandler(chosen_fours_csv_path, chosen_fours_sql_path, 'chosen_fours_db')
        chosen_fours_obj.data_init()

        chosen_fours_obj.plot_data()
        self.m_train_data_obj.plot_data()
        self.m_test_data_obj.plot_data()

    def plot_chosen_ideal_funcs_and_train_data(self) :
        # Combine plots
        training_data = self.m_train_data_obj.load_from_db('train_db')
        merged_df = pd.merge(training_data, self.m_chosen_fours_data, on='x')
        print(merged_df)

        # Save merged data frame from into a new csv file
        csv_path_result_combined = output_path + 'train_and_best_4_combined.csv'
        merged_df.to_csv(csv_path_result_combined, index=False)

        # Create new data object and plot the merged data frame
        sql_db_path_combined = output_path + 'train_and_best_4_combined.db'
        combined_obj = DataSetHandler(csv_path_result_combined, sql_db_path_combined, 'train_and_best_4_combined_db')
        combined_obj.data_init()
        combined_obj.plot_data()

    def run(self):
        self.data_init()
        self.find_ideal_functions()
        self.test_data_evaluation()
        self.plot_chosen_ideal_funcs()
        self.plot_chosen_ideal_funcs_and_train_data()

if __name__ == '__main__':
    input_path = './data_set/dataset_1/'
    output_path = '../output/dataset_1/'

    task_processor = TaskProcessor(input_path, output_path)
    task_processor.run()

