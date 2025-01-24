import pandas as pd
from sqlalchemy import create_engine
from utils.exception import DataSetHandlerException

class SQLiteDataHandler():
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.m_db_path = db_path

    def save_to_db(self, table_name, data):
        """
        Function to save data to sqlite database.
        """
        try:
            data.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except Exception as e:
            raise DataSetHandlerException(f"Error saving data to {table_name}: {e}")

    def load_from_db(self, table_name):
        """
        Function to load data from sqlite database.
        """
        try:
            return pd.read_sql_table(table_name, self.engine)
        except Exception as e:
            raise DataSetHandlerException(f"Error loading data from {table_name}: {e}")

    def plot_data(self):
        """
        Function to visualize the data.
        """
        pass