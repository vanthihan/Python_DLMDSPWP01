from bokeh.layouts import row
from bokeh.plotting import figure, show
import pandas as pd

from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataSetHandler import TestDataSetHandler
from utils.exception import DataSetHandlerException

def main(dataset_root_path) :
    try:
        # Initialize data objects
        csv_path_train = dataset_root_path + 'train.csv'
        csv_path_ideal = dataset_root_path + 'ideal.csv'
        csv_path_test = dataset_root_path + 'test.csv'

        sql_db_path_train = dataset_root_path + 'train.db'
        sql_db_path_ideal = dataset_root_path + 'ideal.db'
        sql_db_path_test = dataset_root_path + 'test.db'

        train_data_obj = DataSetHandler(csv_path_train , sql_db_path_train, 'train_db')
        ideal_data_obj = DataSetHandler(csv_path_ideal , sql_db_path_ideal, 'ideal_db')
        test_data_obj = TestDataSetHandler(csv_path_test , sql_db_path_test, 'test_db')

        # Prepare data from inputed csv files
        train_data_obj.data_invoke()
        ideal_data_obj.data_invoke()
        test_data_obj.data_invoke()

        # Get SQLite data from initialized databases
        training_data = train_data_obj.load_from_db('train_db')
        ideal_data = ideal_data_obj.load_from_db('ideal_db')
        test_data = test_data_obj.load_from_db('test_db')

        print(training_data)
        print(ideal_data)

        # Select ideal functions
        ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
        best_4_ideal_funcs = ideal_func_selector_obj.select_ideal_functions()

        # Below are best 4 functions which best fit to provided train functions
        print(best_4_ideal_funcs)

        # Save best fit functions to an new csv file
        csv_path_best_4 = dataset_root_path + 'best_4.csv'
        sql_db_path_best_4 = dataset_root_path + 'best_4.db'
        best_4_ideal_funcs.to_csv(csv_path_best_4, index=False)

        # Create new datset hander object for best fit ideal functions
        best_4_ideal_funcs_obj = DataSetHandler(csv_path_best_4, sql_db_path_best_4, 'best_4_db')
        best_4_ideal_funcs_obj.data_invoke()

        best_4_ideal_funcs_obj.plot_data()
        train_data_obj.plot_data()
        test_data_obj.plot_data()


        # Combine plots
        merged_df = pd.merge(training_data, best_4_ideal_funcs, on='x')
        print(merged_df)

        csv_path_result_combined = dataset_root_path + 'csv_path_result_combined.csv'
        merged_df.to_csv(csv_path_result_combined, index=False)

        sql_db_path_combined = dataset_root_path + 'csv_path_result_combined.db'
        combined_obj = DataSetHandler(csv_path_result_combined, sql_db_path_combined, 'combined_db')
        combined_obj.data_invoke()
        combined_obj.plot_data()


        # Evaluate test data
        # evaluator = TestDataEvaluator(test_data, ideal_data, chosen_functions, training_data)
        # results = evaluator.evaluate()

    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == '__main__':
    data_set_path_1 = './data_set/dataset_1/'
    data_set_path_2 = './data_set/dataset_2/'

    main(data_set_path_1)
    # main(data_set_path_2)

    
