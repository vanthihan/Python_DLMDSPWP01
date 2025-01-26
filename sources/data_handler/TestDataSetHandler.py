import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.io import save

class TestDataSetHandler():
    def __init__(self, train_data, the_chosen_fours):
        self.m_train_data = train_data
        self.m_the_chosen_fours = the_chosen_fours
        self.m_test_result_OK = None
        self.m_test_result_NOK = None

    def evaluate(self, test_data):
        """
        The criterion for mapping the individual test case to the four ideal functions is
        that the existing maximum deviation of the calculated regression does not exceed the largest deviation between 
        training dataset (A) and the ideal function (C) chosen for it by more than factor sqrt(2)
        """
        test_x = float(test_data['x'])
        test_y = float(test_data['y'])

        train_y_value_from_x = {}
        the_chosen_fours_y_value_from_x = {}
        the_chosen_fours_and_test_deviation = {}
        max_allowed_deviation = {}

        for i in range(4):
            train_y_value_from_x[i] = np.interp(test_x, self.m_train_data['x'], self.m_train_data.iloc[:, i + 1])
            the_chosen_fours_y_value_from_x[i] = np.interp(test_x, self.m_the_chosen_fours['x'], self.m_the_chosen_fours.iloc[:, i + 1])

            max_allowed_deviation[i] = np.sqrt(2) * (self.m_train_data.iloc[:, i + 1] - self.m_the_chosen_fours.iloc[:, i + 1]).abs().max()
            print(f"max_allowed_deviation[i] is {max_allowed_deviation[i]}")

            the_chosen_fours_and_test_deviation[i] = abs(test_y - the_chosen_fours_y_value_from_x[i])

        for i in range(4):
            if(the_chosen_fours_and_test_deviation[i] <= max_allowed_deviation[i]):
                print(f"Test data passed")
                return True

        return False

    def plot_data(self, data, figure_path):
        output_file(figure_path)

        plot = figure(title="Test Data Visualiztion", x_axis_label='x', y_axis_label='y', width=1200, height=800)
        plot.scatter(data['x'], data['y'], size=10, color="red", alpha=1, legend_label="Test point data")

        # for i, row in data.iterrows():
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

