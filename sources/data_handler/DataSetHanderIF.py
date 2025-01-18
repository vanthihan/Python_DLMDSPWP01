from typing import Union
import pandas as pd
from bokeh.plotting import Figure

class DatasetHandlerIF():
    """
    Abstract base class for dataset handlers.

    Provides a common interface for working with various datasets.
    """

    def LoadData(self, filePath: str) -> None:
        """
        Loads data from a CSV file into a DataFrame.
        
        :param filePath: Path to the CSV file
        """
        pass

    def ValidateData(self) -> None:
        """
        Validates the dataset to ensure it meets the required structure.
        """
        pass

    def SumOfDeviation(self, referenceData: pd.DataFrame) -> Union[float, pd.DataFrame]:
        """
        Calculates the sum of deviations between the dataset and a reference dataset.
        
        :param referenceData: A DataFrame to calculate deviations against
        :return: Sum of deviations or a DataFrame with deviation details
        """
        pass

    def PlotDataset(self, title: str, xLabel: str, yLabel: str) -> Figure:
        """
        Generates a Bokeh plot of the dataset.

        :param title: Title of the plot
        :param xLabel: Label for the x-axis
        :param yLabel: Label for the y-axis
        :return: A Bokeh Figure object
        """
        pass

    def SaveToDatabase(self, dbConnection, tableName: str) -> None:
        """
        Saves the dataset to a database table.

        :param dbConnection: A database connection object
        :param tableName: The name of the table to save the data
        """
        pass
