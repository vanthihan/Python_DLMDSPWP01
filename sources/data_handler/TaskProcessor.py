import pandas as pd
import csv
from bokeh.models import Label
from bokeh.plotting import figure, show, output_file
from bokeh.io import save

from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataSetHandler import TestDataSetHandler
from utils.DataInfoType import DataInfoType

from utils.DataException import DataException
from utils.DataException import FileNotFoundException
from utils.DataException import VisualizationException

class TaskProcessor:
    def __init__(self, input_path, output_path):
        """
        Initialize member objects to use within the class
        """
        self.m_input_path = input_path
        self.m_output_path = output_path

        self.m_train_data_obj = None
        self.m_ideal_data_obj = None
        self.m_test_data_obj = None

        self.m_the_fours_ideal_funcs = None
        self.m_ideal_func_selector_obj = None
        self.m_test_result_data_obj = None

    def data_init(self):
        """
            Load training data and ideal data from inputed csv files
            and store into sql database files and tables
        """
        try:
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

        except (DataException, FileNotFoundException) as e:
                print(f"ERROR: {e}")

    def find_ideal_functions(self):
        """
        This function will help to select the best fours function which has minimal deviation
        based on least squared method.

        The result is an sql table stored in /output/the_fours_ideal.csv
        """
        try:
            # Get SQLite data from initialized databases
            training_data = self.m_train_data_obj.load_from_db('train_table')
            ideal_data = self.m_ideal_data_obj.load_from_db('ideal_table')

            # Select ideal functions
            self.m_ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
            self.m_the_fours_ideal_funcs = self.m_ideal_func_selector_obj.find_ideal_functions()

            # Save the fours ideal function into a csv file
            the_fours_ideal_csv_path = self.m_output_path + 'the_fours_ideal.csv'
            self.m_the_fours_ideal_funcs.to_csv(the_fours_ideal_csv_path, index=False)

        except (DataException, FileNotFoundException) as e:
                print(f"ERROR: {e}")

    def test_data_evaluation(self):
        """
        Test data x-y pair will be loaded line-by-line from test.csv fild and will be
        evaluation witht the fours ideal and traning dataset

        The test status passed or NOT passed will be stored in 2 data frame which will be used later for test data visualiztion

        The final result is a data table which follows the format as x, y, deviation and the fours ideal function name
        and will be stored in [result.csv/db] inside ouput folder

        """
        try:
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

            # Save test result into 2 separated data frames
            test_result_OK_df = pd.DataFrame(test_result_OK[1:])
            test_result_OK_df['x'] = pd.to_numeric(test_result_OK_df['x'])
            test_result_OK_df['y'] = pd.to_numeric(test_result_OK_df['y'])

            test_result_NOK_df = pd.DataFrame(test_result_NOK[1:])
            test_result_NOK_df['x'] = pd.to_numeric(test_result_NOK_df['x'])
            test_result_NOK_df['y'] = pd.to_numeric(test_result_NOK_df['y'])

            self.m_test_data_obj.m_test_result_OK = test_result_OK_df
            self.m_test_data_obj.m_test_result_NOK = test_result_NOK_df

            # Get test result SQL data table with format x, y, deviation, ideal function name
            result_csv_path = self.m_output_path + 'test_result.csv'
            result_sql_path = self.m_output_path + 'test_result.db'
            result_sql_name = 'test_result_table'
            sql_result_table = self.m_test_data_obj.get_test_result_data(result_sql_path, result_sql_name)

            # Save test result into a new csv file
            sql_result_table.to_csv(result_csv_path, index=False)
            print(f"Test Result Data saved to: {result_csv_path}")

        except (DataException, FileNotFoundException) as e:
                print(f"ERROR: {e}")

    def visualize_training_data(self) :
        """
        Create a plot to visualize the training data only.
        Plot will be saved to /output/train_data.html
        """
        try:
            plot = self.m_train_data_obj.plot_data()

            figure_path = self.m_output_path + 'train_data.html'
            output_file(figure_path)
            save(plot)
            print(f"Training data's plot saved at: {figure_path}")

        except (VisualizationException) as e:
                print(f"ERROR: {e}")

    def visualize_chosen_ideal_funcs(self) :
        """
        Create a plot to visualize the best fours ideal function selected from 50 functions only.
        Plot will be saved to /output/the_fours_ideal.html
        """
        try:
            # Create new datset hander object for best fit ideal functions
            the_fours_ideal_csv_path = self.m_output_path + 'the_fours_ideal.csv'
            the_fours_ideal_sql_path = self.m_output_path + 'the_fours_ideal.db'
            fours_ideal_data_info = DataInfoType(the_fours_ideal_csv_path, the_fours_ideal_sql_path, "the_fours_ideal_table")

            the_fours_ideal_obj = DataSetHandler(fours_ideal_data_info)
            the_fours_ideal_obj.data_init()

            # Plot the data
            plot = the_fours_ideal_obj.plot_data()

            note_text = "Description:\n"
            for train_col, (ideal_func, deviation) in self.m_ideal_func_selector_obj.m_the_fours_ideal.items():
                note_text += (f"The deviation of the chosen ideal [{ideal_func}] is: [{deviation:.4f}]\n")

            note = Label(x=10, y=10, x_units='screen', y_units='screen',
                        text=note_text, text_font_size="12pt",
                        text_color="black", background_fill_color="white", background_fill_alpha=1)
            plot.add_layout(note, 'right')

            figure_path = self.m_output_path + 'the_fours_ideal.html'
            output_file(figure_path)
            save(plot)
            print(f"The fours ideal function's plot saved at: {figure_path}")
        except (VisualizationException) as e:
            print(f"ERROR: {e}")

    def visualize_chosen_ideal_funcs_and_train_data(self) :
        """
        This function will combine data of the training data the best fours ideal function data.

        Then create a plot to visualize both data.
        Data will be saved to /output/train_and_the_fours_ideal.csv/db
        Plot will be saved to /output/train_and_the_fours_ideal.html
        """
        try:
            # Combine plots
            training_data = self.m_train_data_obj.load_from_db('train_table')
            merged_df = pd.merge(training_data, self.m_the_fours_ideal_funcs, on='x')
            # print(merged_df)

            # Save merged data frame from into a new csv file
            csv_path_result_combined = self.m_output_path + 'train_and_the_fours_ideal.csv'
            merged_df.to_csv(csv_path_result_combined, index=False)

            # Create new data object and plot the merged data frame
            sql_sql_path_combined = self.m_output_path + 'train_and_the_fours_ideal.db'
            combined_data_info = DataInfoType(csv_path_result_combined, sql_sql_path_combined, "train_and_the_fours_ideal_table")

            combined_obj = DataSetHandler(combined_data_info)
            combined_obj.data_init()

            # Plot the data
            plot = combined_obj.plot_data()

            # Add a note to the plot
            note_text = "Description:\n"
            for train_col, (ideal_func, deviation) in self.m_ideal_func_selector_obj.m_the_fours_ideal.items():
                note_text += (f"Ideal [{ideal_func}] matched to Train [{train_col}] - Min Deviation: [{deviation:.4f}]\n")

            note = Label(x=10, y=10, x_units='screen', y_units='screen',
                        text=note_text, text_font_size="12pt",
                        text_color="black", background_fill_color="white", background_fill_alpha=1)
            plot.add_layout(note, 'right')

            figure_path = self.m_output_path + 'train_and_the_fours_ideal.html'
            output_file(figure_path)
            save(plot)
            print(f"The training and fours ideal function's plot saved at: {figure_path}")
        except (DataException, VisualizationException) as e:
            print(f"ERROR: {e}")

    def visualize_test_result_data(self) :
        """
        This function will combine data of the training data the best fours ideal function data.

        Then create a plot to visualize both data.
        Data will be saved to /output/train_and_the_fours_ideal.csv/db
        Plot will be saved to /output/train_and_the_fours_ideal.html
        """
        try:
            figure_path = self.m_output_path + 'test_result.html'
            self.m_test_data_obj.plot_data(figure_path)
        except (VisualizationException) as e:
            print(f"ERROR: {e}")

    def run(self):
        """
        Run the task sequentially
        """
        try:
            self.data_init()
            self.find_ideal_functions()
            self.test_data_evaluation()

            self.visualize_training_data()
            self.visualize_chosen_ideal_funcs()
            self.visualize_chosen_ideal_funcs_and_train_data()
            self.visualize_test_result_data()

        except (DataException, FileNotFoundException, VisualizationException) as e:
            print(f"ERROR: {e}")