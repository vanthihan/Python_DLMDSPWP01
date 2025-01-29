from src.task_processor import TaskProcessor
from src.utils.data_exception import DataException

if __name__ == '__main__':
    try:
        """
        - By provding the path to input dataset file, calling the task processor will 
        select the best fours ideals function from ideal dataset which matched to 4 function in
        training dataset.
        - After that, the test data from test csv file will be loaded line-by-line and return the 
        result whether these test x-y pair is passed the condition with 1 of 4 ideals function.
        - All database and plots will be saved to [output] path foleder.

        input_path: provided data set csv file paths of training, ideal and test dataset
        output_path: folder to store all figure, generated sql database and csv files
        """
        input_path = '../input/dataset_1/'
        output_path = '../output/dataset_1/'

        task_processor = TaskProcessor(input_path, output_path)
        task_processor.run()

    except DataException:
            raise DataException("Error handling data")
    except Exception as e:
        raise RuntimeError(f"Unexpected error in main: {e}")
