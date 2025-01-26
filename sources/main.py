import pandas as pd
import csv

from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataSetHandler import TestDataSetHandler
from data_handler.SQLiteDataHandler import SQLiteDataHandler
from utils.exception import DataSetHandlerException
from utils.DataInfoType import DataInfoType

class TaskProcessor:
    def __init__(self, input_path, output_path):
        self.m_input_path = input_path
        self.m_output_path = output_path
        self.m_train_data_obj = None
        self.m_ideal_data_obj = None
        self.m_test_data_obj = None
        self.m_test_result_data_obj = None
        self.m_the_fours_ideal_funcs = None

    def data_init(self):
        csv_path_train = self.m_input_path + 'train.csv'
        csv_path_ideal = self.m_input_path + 'ideal.csv'

        sql_sql_path_train = self.m_output_path + 'train.db'
        sql_sql_path_ideal = self.m_output_path + 'ideal.db'

        training_data_info = DataInfoType(csv_path_train, sql_sql_path_train, "train_table")
        ideal_data_info = DataInfoType(csv_path_ideal, sql_sql_path_ideal, "ideal_table")

        self.m_train_data_obj = DataSetHandler(training_data_info)
        self.m_ideal_data_obj = DataSetHandler(ideal_data_info)

        self.m_train_data_obj.data_init()
        self.m_ideal_data_obj.data_init()

    def find_ideal_functions(self):
        # Get SQLite data from initialized databases
        training_data = self.m_train_data_obj.load_from_db('train_table')
        ideal_data = self.m_ideal_data_obj.load_from_db('ideal_table')

        # Select ideal functions
        ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
        self.m_the_fours_ideal_funcs = ideal_func_selector_obj.find_ideal_functions()

    def test_data_evaluation(self):
        # Prepare training data and the chosen fours  from ideal data
        training_data = self.m_train_data_obj.load_from_db('train_table')
        the_chosen_fours = self.m_the_fours_ideal_funcs
        csv_path_test = self.m_input_path + 'test.csv'
        self.m_test_data_obj = TestDataSetHandler(training_data, the_chosen_fours)

        # Open the CSV file and read line-by-line
        test_result_OK = []
        test_result_NOK = []
        with open(csv_path_test, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Get the header (1st line)
            test_result_OK.append(csv_reader.fieldnames)
            test_result_NOK.append(csv_reader.fieldnames)

            # Start evaluate the test data from 2nd line
            for test_data_row in csv_reader:
                is_passed = self.m_test_data_obj.evaluate(test_data_row)
                if(True == is_passed) :
                    test_result_OK.append(test_data_row)
                else:
                    test_result_NOK.append(test_data_row)

        test_result_OK_df = pd.DataFrame(test_result_OK[1:])
        test_result_OK_df['x'] = pd.to_numeric(test_result_OK_df['x'])
        test_result_OK_df['y'] = pd.to_numeric(test_result_OK_df['y'])

        test_result_NOK_df = pd.DataFrame(test_result_NOK[1:])
        test_result_NOK_df['x'] = pd.to_numeric(test_result_NOK_df['x'])
        test_result_NOK_df['y'] = pd.to_numeric(test_result_NOK_df['y'])

        self.m_test_data_obj.m_test_result_OK = test_result_OK_df
        self.m_test_data_obj.m_test_result_NOK = test_result_NOK_df

    def plot_chosen_ideal_funcs(self) :
        # Create new datset hander object for best fit ideal functions
        the_fours_ideal_csv_path = output_path + 'the_fours_ideal.csv'
        the_fours_ideal_sql_path = output_path + 'the_fours_ideal.db'
        training_data_info = DataInfoType(the_fours_ideal_csv_path, the_fours_ideal_sql_path, "the_fours_ideal_table")

        self.m_the_fours_ideal_funcs.to_csv(the_fours_ideal_csv_path, index=False)

        the_fours_ideal_obj = DataSetHandler(training_data_info)
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
        test_result_OK_figure_path = self.m_output_path + 'test_result_OK.html'
        test_result_NOK_figure_path = self.m_output_path + 'test_result_NOK.html'

        self.m_test_data_obj.plot_data(self.m_test_data_obj.m_test_result_OK, test_result_OK_figure_path)
        self.m_test_data_obj.plot_data(self.m_test_data_obj.m_test_result_NOK, test_result_NOK_figure_path)

    def run(self):
        self.data_init()
        self.find_ideal_functions()
        self.test_data_evaluation()
 
        self.plot_chosen_ideal_funcs()
        self.plot_chosen_ideal_funcs_and_train_data()
        self.plot_test_data()

if __name__ == '__main__':
    input_path = './data_set/dataset_1/'
    output_path = '../output/dataset_1/'

    task_processor = TaskProcessor(input_path, output_path)
    task_processor.run()

