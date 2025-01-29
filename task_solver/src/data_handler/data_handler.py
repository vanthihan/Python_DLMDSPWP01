import pandas as pd
from src.data_handler.sql_data_handler import SQLiteDataHandler
from bokeh.plotting import figure

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
            df = pd.read_csv(self.m_csv_path)  # Loading the CSV
            if df.empty:
                raise ValueError(f"CSV file is empty: {self.m_csv_path}")

            self.save_to_db(self.m_sql_table_name, df)  # Save data to DB
            return self.load_from_db(self.m_sql_table_name)

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.m_csv_path}")
        except pd.errors.ParserError:
            raise ValueError(f"Error parsing CSV file: {self.m_csv_path}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during data initialization: {e}")

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

        except ValueError as ve:
            raise ValueError(f"Plotting error: {ve}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during plotting: {e}")