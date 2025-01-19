from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bokeh.plotting import figure, show
from bokeh.io import output_file
import pandas as pd

from data_handler.DataSetHandlerIF import DataSetHandlerIF
from utils.exception import DataSetHandlerException


class TrainingDataSetHandler(DataSetHandlerIF):
    """
    Training dataset handler implementation.
    """
    def __init__(self, data_path):
        super().__init__(data_path)

    def load_data(self):
        """
        Load CSV data into a Pandas DataFrame.
        """
        try:
            self.data = pd.read_csv(self.data_path)
            print("Training Dataset loaded successfully!")
            print(self.data)

        except Exception as e:
            raise DataSetHandlerException(f"Failed to load data: {e}")

    def visualize_data(self):
        """
        Visualize the dataset columns using Bokeh.
        """

        output_file("training_data_plot_multiple_y.html")
        self.df = pd.DataFrame(self.data)
        p = figure(title="Training Data Visualization", x_axis_label='X', y_axis_label='Y', width=800, height=400)

        for column in self.df.columns:
            if column.startswith('y'):  # Checks if the column name starts with 'y'
                p.line(self.df['x'], self.df[column], legend_label=column, line_width=2)

        p.legend.location = "top_left"
        show(p)

        if self.data is None:
            raise DataSetHandlerException("Data not loaded. Please load the data first.")
