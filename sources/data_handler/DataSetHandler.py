import pandas as pd
from data_handler.SQLiteDataHandler import SQLiteDataHandler

class DataSetHandler(SQLiteDataHandler):
    def __init__(self, csv_path, db_path, db_name):
        super().__init__(db_path)
        self.m_csv_path = csv_path
        self.m_db_name = db_name

    def data_invoke(self):
        try:
            self.save_to_db(self.m_db_name, pd.read_csv(self.m_csv_path))
            return self.load_from_db(self.m_db_name)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.m_csv_path}")
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {e}")