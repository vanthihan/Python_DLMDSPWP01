import pandas as pd
from data_handler.SQLiteDataHandler import SQLiteDataHandler
from bokeh.plotting import figure, show, output_file
from bokeh.io import save

class DataSetHandler(SQLiteDataHandler):
    def __init__(self, data_info):
        super().__init__(data_info.sql_path)
        self.m_csv_path = data_info.csv_path
        self.m_sql_table_name = data_info.sql_table_name

    def data_init(self):
        try:
            self.save_to_db(self.m_sql_table_name, pd.read_csv(self.m_csv_path))
            return self.load_from_db(self.m_sql_table_name)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.m_csv_path}")
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {e}")

    def plot_data(self):
        try:
            figure_path = self.m_sql_path[:-3] + '.html' # Removing '.db.' from the sql_path
            output_file(figure_path)

            # Define a custom color palette
            palette = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
                "#bcbd22", "#17becf"
            ]

            plot = figure(title=f"{self.m_sql_table_name[:-3].replace("_", " ")} Data Visualiztion",
                          x_axis_label="x", y_axis_label="y", width=1200, height=800)

            data_to_plot = self.load_from_db(self.m_sql_table_name)
            for i, y_col in enumerate(data_to_plot.columns[1:]):
                # Custom color for each function
                color = palette[i % len(palette)]
                plot.line(data_to_plot['x'], data_to_plot[y_col],
                    legend_label=f"{y_col}",
                    line_width=2, color=color)
                
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

            save(plot)
            print(f"Plot file saved to: {figure_path}")

        except Exception as e:
            raise ValueError(f"{e}")