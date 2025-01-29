import pandas as pd
from data_handler.SQLiteDataHandler import SQLiteDataHandler
from bokeh.plotting import figure, show, output_file
from bokeh.io import save
from bokeh.models import Label

from utils.DataException import DataException
from utils.DataException import FileNotFoundException

class DataSetHandler(SQLiteDataHandler):
    def __init__(self, data_info):
        """
        Init data member variables
        """
        super().__init__(data_info.sql_path)
        self.m_csv_path = data_info.csv_path
        self.m_sql_table_name = data_info.sql_table_name

    def data_init(self):
        """
        Save data from inputed csv file into sql file
        """
        try:
            self.save_to_db(self.m_sql_table_name, pd.read_csv(self.m_csv_path))
            return self.load_from_db(self.m_sql_table_name)
        except FileNotFoundException:
            raise FileNotFoundException(f"File not found: {self.m_csv_path}")
        except DataException:
            raise DataException(f"Error loading CSV file")

    def plot_data(self):
        """
        Visualize data
        """
        try:
            # Define a custom color list
            color_list = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
            ]

            plot = figure(title=f"{self.m_sql_table_name.replace("_", " ")} plot",
                          x_axis_label="x", y_axis_label="y", width=1500, height=800)

            data_to_plot = self.load_from_db(self.m_sql_table_name)
            for i, y_col in enumerate(data_to_plot.columns[1:]):
                # Custom color for each function
                color = color_list[i % len(color_list)]
                plot.line(data_to_plot['x'], data_to_plot[y_col], legend_label=f"{y_col}", line_width=2, color=color)
                
            plot.xaxis.axis_label_text_font_size = "16pt"
            plot.xaxis.axis_label_text_font_style = "bold"
            plot.xaxis.axis_label_text_color = "darkblue"

            plot.yaxis.axis_label_text_font_size = "16pt"
            plot.yaxis.axis_label_text_font_style = "bold"
            plot.yaxis.axis_label_text_color = "darkred"
                
            plot.legend.title = "Legend"
            plot.legend.label_text_font_size = "12pt"
            plot.legend.title_text_font_size = "12pt"
            plot.add_layout(plot.legend[0], 'right')

            return plot

        except DataException as e:
            raise DataException(f"{e}")