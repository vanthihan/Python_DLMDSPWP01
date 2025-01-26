from bokeh.layouts import row
from bokeh.plotting import figure, show
import pandas as pd

from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataSetHandler import TestDataSetHandler
from utils.exception import DataSetHandlerException
from utils.DataInfoType import DataInfoType

class TaskProcessor:
    def __init__(self, input_path, output_path):
        self.m_input_path = input_path
        self.m_output_path = output_path
        self.m_train_data_obj = None
        self.m_ideal_data_obj = None
        self.m_test_data_obj = None
        self.m_the_fours_ideal_funcs = None

    def data_init(self):
        csv_path_train = self.m_input_path + 'train.csv'
        csv_path_ideal = self.m_input_path + 'ideal.csv'

        sql_sql_path_train = self.m_output_path + 'train.db'
        sql_sql_path_ideal = self.m_output_path + 'ideal.db'

        trainning_data_info = DataInfoType(csv_path_train, sql_sql_path_train, "train_table")
        ideal_data_info = DataInfoType(csv_path_ideal, sql_sql_path_ideal, "ideal_table")

        self.m_train_data_obj = DataSetHandler(trainning_data_info)
        self.m_ideal_data_obj = DataSetHandler(ideal_data_info)

        self.m_train_data_obj.data_init()
        self.m_ideal_data_obj.data_init()

    def find_ideal_functions(self):
        # Get SQLite data from initialized databases
        training_data = self.m_train_data_obj.load_from_db('train_table')
        ideal_data = self.m_ideal_data_obj.load_from_db('ideal_table')
        # print(training_data, ideal_data)

        # Select ideal functions
        ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
        self.m_the_fours_ideal_funcs = ideal_func_selector_obj.find_ideal_functions()
        # print(self.m_the_fours_ideal_funcs)

    def test_data_evaluation(self):
        csv_path_test = self.m_input_path + 'test.csv'
        sql_sql_path_test = self.m_output_path + 'test.db'
        test_data = DataInfoType(csv_path_test, sql_sql_path_test, "test_table")
        self.m_test_data_obj = TestDataSetHandler(test_data)

        test_result = self.m_test_data_obj.evaluate(self.m_the_fours_ideal_funcs)

    def plot_chosen_ideal_funcs(self) :
        # Create new datset hander object for best fit ideal functions
        the_fours_ideal_csv_path = output_path + 'the_fours_ideal.csv'
        the_fours_ideal_sql_path = output_path + 'the_fours_ideal.db'
        trainning_data_info = DataInfoType(the_fours_ideal_csv_path, the_fours_ideal_sql_path, "the_fours_ideal_table")

        self.m_the_fours_ideal_funcs.to_csv(the_fours_ideal_csv_path, index=False)

        the_fours_ideal_obj = DataSetHandler(trainning_data_info)
        the_fours_ideal_obj.data_init()

        # Plot the data
        the_fours_ideal_obj.plot_data()

    def plot_chosen_ideal_funcs_and_train_data(self) :
        # Combine plots
        training_data = self.m_train_data_obj.load_from_db('train_table')
        merged_df = pd.merge(training_data, self.m_the_fours_ideal_funcs, on='x')
        # print(merged_df)

        # Save merged data frame from into a new csv file
        csv_path_result_combined = output_path + 'train_and_the_fours_ideal.csv'
        merged_df.to_csv(csv_path_result_combined, index=False)

        # Create new data object and plot the merged data frame
        sql_sql_path_combined = output_path + 'train_and_the_fours_ideal.db'
        combined_data_info = DataInfoType(csv_path_result_combined, sql_sql_path_combined, "train_and_the_fours_ideal_table")

        combined_obj = DataSetHandler(combined_data_info)
        combined_obj.data_init()
        combined_obj.plot_data()

    def plot_test_data(self) :
        self.m_test_data_obj.plot_data()

    def run(self):
        self.data_init()
        self.find_ideal_functions()
        # self.test_data_evaluation()

        self.plot_chosen_ideal_funcs()
        self.plot_chosen_ideal_funcs_and_train_data()
        # self.plot_test_data()

if __name__ == '__main__':
    input_path = './data_set/dataset_1/'
    output_path = '../output/dataset_1/'

    task_processor = TaskProcessor(input_path, output_path)
    task_processor.run()

