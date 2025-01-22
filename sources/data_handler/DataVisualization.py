from bokeh.plotting import figure, show, output_file
from bokeh.io import save

class DataVisualization:
    @staticmethod
    def plot_data(training_data, test_data, ideal_functions, selected_functions, results):
        output_file("visualization.html")

        # Define a color palette
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", 
            "#bcbd22", "#17becf"
        ]

        p = figure(title="Data Visualization", x_axis_label="x", y_axis_label="y", width=800, height=600)

        # Plot training data with custom colors
        for i, y_col in enumerate(training_data.columns[1:]):
            color = palette[i % len(palette)]
            p.line(training_data['x'], training_data[y_col], 
                   legend_label=f"Training {y_col}", 
                   line_width=2, color=color)

        # Plot ideal functions with custom colors
        for i, ideal_col in enumerate(selected_functions.values()):
            color = palette[(i + len(training_data.columns) - 1) % len(palette)]
            p.line(ideal_functions['x'], ideal_functions[ideal_col], 
                   legend_label=f"Ideal {ideal_col}", 
                   line_dash="dotted", color=color)

        # Plot test data
        p.circle(test_data['x'], test_data['y'], 
                 legend_label="Test Data", 
                 color="red", size=8)

        # Plot matched results
        for x, y, ideal_col, deviation in results:
            p.circle([x], [y], 
                     legend_label=f"Matched to {ideal_col}", 
                     size=6, color="green")

        p.legend.click_policy = "hide"
        save(p)
        show(p)