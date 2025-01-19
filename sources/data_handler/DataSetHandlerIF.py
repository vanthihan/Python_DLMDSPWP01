import pandas as pd
from abc import ABC, abstractmethod

class DataSetHandlerIF(ABC):
    """
    Abstract base class for dataset handlers.
    """
    def __init__(self, data_path):
        """
        Initialize the dataset handler with a path to a CSV file.

        :param data_path: Path to the CSV file.
        """
        self.data_path = data_path
        self.data = None

    @abstractmethod
    def load_data(self):
        """
        Load data from a CSV file.
        """
        pass

    @abstractmethod
    def visualize_data(self):
        """
        Visualize the dataset.
        """
        pass