import pandas as pd
from data_handler.SQLiteDataHandler import SQLiteDataHandler
from bokeh.plotting import figure, show, output_file
from bokeh.io import save

from data_handler.DataSetHandler import DataSetHandler

class TestDataSetHandler(DataSetHandler):
    def __init__(self, csv_path, db_path, db_name):
        super().__init__(csv_path, db_path, db_name)

    def plot_data(self):
        try:
            figure_path = self.m_db_path[:-3] + '.html' # Removing '.db.' from the db_path
            print(figure_path)
            output_file(figure_path)

            # Define a color palette
            palette = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", 
                "#bcbd22", "#17becf"
            ]

            plot = figure(title=f"{self.m_db_name[:-3].replace("_", " ")} Data Visualiztion",
                          x_axis_label="x", y_axis_label="y", width=1000, height=1000)

            data_to_plot = self.load_from_db(self.m_db_name)
            for i, y_col in enumerate(data_to_plot.columns[1:]):
                # Custom color for each function
                color = palette[i % len(palette)]
                plot.line(data_to_plot['x'], data_to_plot[y_col], legend_label=f"Training {y_col}", line_width=2, color=color)

            save(plot)

        except Exception as e:
            raise ValueError(f"{e}")
        
    def evaluate(self):
        print("Evaluate test data")