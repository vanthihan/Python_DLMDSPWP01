from data_handler.DataSetHandler import DataSetHandler
from data_handler.IdealFunctionSelector import IdealFunctionSelector
from data_handler.TestDataEvaluator import TestDataEvaluator
from data_handler.DataVisualization import DataVisualization
from utils.exception import DataSetHandlerException

if __name__ == '__main__':
    try:
        # Initialize data objects
        train_data_obj = DataSetHandler('./data_set/dataset_1/train.csv' ,'./data_set/dataset_1/train.db', 'train_db')
        ideal_data_obj = DataSetHandler('./data_set/dataset_1/ideal.csv' ,'./data_set/dataset_1/ideal.db', 'ideal_db')
        test_data_obj = DataSetHandler('./data_set/dataset_1/test.csv' ,'./data_set/dataset_1/test.db', 'test_db')

        # Prepare data from inputed csv files
        train_data_obj.data_invoke()
        ideal_data_obj.data_invoke()
        test_data_obj.data_invoke()

        # Get SQLite data from initialized databases
        training_data = train_data_obj.load_from_db('train_db')
        ideal_data = ideal_data_obj.load_from_db('ideal_db')
        test_data = test_data_obj.load_from_db('test_db')

        # Select ideal functions
        ideal_func_selector_obj = IdealFunctionSelector(training_data, ideal_data)
        best_4_ideal_funcs = ideal_func_selector_obj.select_ideal_functions()

        print(best_4_ideal_funcs)
        best_4_ideal_funcs.to_csv('./data_set/dataset_1/best_4_ideal_funcs.csv', index=False)

        # Adding new data table for selected 4 functions into ideal database
        ideal_data_obj.save_to_db('best_4_ideal_funcs_db', best_4_ideal_funcs)

        # Verify saved selected funcs
        print(ideal_data_obj.load_from_db('best_4_ideal_funcs_db'))


        # Evaluate test data
        # evaluator = TestDataEvaluator(test_data, ideal_data, chosen_functions, training_data)
        # results = evaluator.evaluate()
        # loader.save_to_db('results', results)

        # Visualize results
        # visualizer = DataVisualization()
        # visualizer.plot_data(training_data, test_data, ideal_data, chosen_functions, results)

    except Exception as e:
        print(f"An error occurred: {e}")
