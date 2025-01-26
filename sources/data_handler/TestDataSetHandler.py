import csv
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.io import save
from data_handler.SQLiteDataHandler import SQLiteDataHandler

class TestDataSetHandler(SQLiteDataHandler):
    def __init__(self, data_info):
        super().__init__(data_info.sql_path)
        self.m_sql_table_name = data_info.sql_table_name

    def evaluate(self, bench_mark):
        """
        The criterion for mapping the individual test case to the four ideal functions is
        that the existing maximum deviation of the calculated regression does not exceed the largest deviation between 
        training dataset (A) and the ideal function (C) chosen for it by more than factor sqrt(2)
        """
        test_result = []
        # test_data = self.load_from_db(self.m_sql_table_name)

        return test_result

    def plot_data(self):
        figure_path = self.m_sql_path[:-3] + '.html' # Removing '.db.' from the sql_path
        output_file(figure_path)
        test_data = self.load_from_db(self.m_sql_table_name)
        print(test_data.columns)

        plot = figure(title="Test Data Visualiztion", x_axis_label='x', y_axis_label='y', width=1200, height=800)
        plot.scatter(test_data['x'], test_data['y'], size=10, color="red", alpha=1, legend_label="Test point data")

        # for i, row in test_data.iterrows():
        #     deviation = np.abs(row['x'] - row['y'])
        #     plot.text(x=row['x'], y=row['y'], text=[f"({deviation:.2f})"], 
        #             text_font_size="10pt", text_align="left", text_baseline="bottom", color="black")


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

        # show(plot)
        save(plot)
        print(f"Plot file saved to: {figure_path}")

