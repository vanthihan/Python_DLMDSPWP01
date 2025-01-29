import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.io import save

from src.data_handler.sql_data_handler import SQLiteDataHandler
from src.utils.data_exception import DataException

class FunctionEvaluator():
    def __init__(self, train_data, the_chosen_fours):
        if train_data is None or the_chosen_fours is None:
            raise ValueError("Training data and ideal functions must not be None.")

        if train_data.empty or the_chosen_fours.empty:
            raise ValueError("Training data and ideal functions must not be empty.")

        self.m_train_data = train_data
        self.m_the_chosen_fours = the_chosen_fours
        self.m_test_result_OK = None    # Contain only x and y value of passed test data
        self.m_test_result_NOK = None   # Contain only x and y value of NOT passed test data
        self.m_test_result_data = []    # Create a test result data which contains x, y, deviation, and ideal function name

    def evaluate(self, test_data):
        """
        The criterion for mapping the individual test case to the four ideal functions is
        that the existing maximum deviation of the calculated regression does not exceed the largest deviation between 
        training dataset (A) and the ideal function (C) chosen for it by more than factor sqrt(2)
        """
        try:
            test_x = float(test_data['x'])
            test_y = float(test_data['y'])
            result = False

            train_y_value_from_x = {}
            the_chosen_fours_y_value_from_x = {}
            the_chosen_fours_and_test_deviation = {}
            max_allowed_deviation = {}

            # Boundary check for x value
            if test_x < self.m_train_data['x'].min() or test_x > self.m_train_data['x'].max():
                return False

            # Interpolating data y from x value
            for i in range(4):
                train_y_value_from_x[i] = np.interp(test_x, self.m_train_data['x'], self.m_train_data.iloc[:, i + 1])
                the_chosen_fours_y_value_from_x[i] = np.interp(test_x, self.m_the_chosen_fours['x'], self.m_the_chosen_fours.iloc[:, i + 1])

                # Calculating the deviation of test_y and the fours ideal y
                the_chosen_fours_and_test_deviation[i] = abs(test_y - the_chosen_fours_y_value_from_x[i])

                # Calculating the maximum deviation of train_y and the fours ideal y
                max_allowed_deviation[i] = np.sqrt(2) * (self.m_train_data.iloc[:, i + 1] - self.m_the_chosen_fours.iloc[:, i + 1]).abs().max()

            the_fours_ideal_col_name = self.m_the_chosen_fours.columns.tolist()  # Convert to a list

            # Test sample evaluation
            for i in range(4):
                # Matched to one of the four functions chosen
                if(the_chosen_fours_and_test_deviation[i] <= max_allowed_deviation[i]):
                    result = True

                    # Save test result along with relevant datas
                    self.m_test_result_data.append({
                        "x": float(test_x),
                        "y": float(test_y),
                        "deviation": float(the_chosen_fours_and_test_deviation[i]),
                        "ideal_func": the_fours_ideal_col_name[i+1]
                    })

            return result
        except DataException:
            raise DataException("Error handling test data during evaluation.")
        except ValueError as ve:
            raise ValueError(f"Invalid test data: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in evaluate method: {e}")

    def plot_data(self, figure_path):
        """
        Creating plot which mixed data of test status and the four ideal functions.
        The test data which passed test criteria will be shown as Green, otherwise,
        not passed test data will be shown as "Red".
        """
        try:
            data_1 = self.m_test_result_OK
            data_2 = self.m_test_result_NOK

            plot = figure(title="Test Data Visualization", x_axis_label='x', y_axis_label='y', width=1200, height=800)

            # Visualize passed and not passed test samples
            plot.scatter(data_1['x'], data_1['y'], size=8, color="green", alpha=1, legend_label="Passed")
            plot.scatter(data_2['x'], data_2['y'], size=8, color="red", alpha=1, legend_label="Not Passed")

            # Define a custom color list
            color_list = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
            ]

            # Visualize the four ideal data functions
            for i, y_col in enumerate(self.m_the_chosen_fours.columns[1:]):
                # Custom color for each function
                color = color_list[i % len(color_list)]
                plot.line(self.m_the_chosen_fours['x'], self.m_the_chosen_fours[y_col], legend_label=f"{y_col}", line_width=2, color=color)

            # Customize the axis labels and other properties for the single plot
            plot.xaxis.axis_label_text_font_size = "16pt"
            plot.xaxis.axis_label_text_font_style = "bold"
            plot.xaxis.axis_label_text_color = "darkblue"

            plot.yaxis.axis_label_text_font_size = "16pt"
            plot.yaxis.axis_label_text_font_style = "bold"
            plot.yaxis.axis_label_text_color = "darkred"

            # Customize the legend for the plot
            plot.legend.title = "Legend"
            plot.legend.label_text_font_size = "12pt"
            plot.legend.title_text_font_size = "12pt"
            plot.add_layout(plot.legend[0], 'right')

            # Save the plot to an HTML file
            output_file(figure_path)
            save(plot)
            show(plot)
            print(f"Plot file saved to: {figure_path}")
        except DataException:
            raise DataException("Error handling data during plot generation.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in plot_data method: {e}")

    def get_test_result_data(self, sql_path, table_name):
        """
        Returning the test result data table as formatted x, y, deviation, and ideal function name
        """
        try:
            sql_data = SQLiteDataHandler(sql_path)
            data_frame = pd.DataFrame(self.m_test_result_data)
            sql_data.save_to_db(table_name, data_frame)

            return sql_data.load_from_db(table_name)
        except DataException:
            raise DataException("Error handling data while saving or loading from database.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in get_test_result_data method: {e}")
