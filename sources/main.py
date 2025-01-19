from data_handler.TrainingDataSetHandler import TrainingDataSetHandler
from utils.exception import DataSetHandlerException

def main():
    """
    Main function to execute the program.
    """
    csv_path = "./data_base/dataset_1/train.csv"
    db_path = "./data_base/dataset_1/train.db"

    try:
        handler = TrainingDataSetHandler(csv_path)
        handler.load_data()
        handler.visualize_data()
        # handler.save_to_database(db_path)
    except DataSetHandlerException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()