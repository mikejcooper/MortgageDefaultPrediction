import numpy as np
import pandas as pd

from DataParser import DataParser
from FeatureExtraction import FeatureExtraction


class DataProcessing:
    """ A class that pre-processes data"""

    def __init__(self):
        """ Example of docstring on the __init__ method.  """

    @property
    def Dataset(self):
        """str: Properties should be documented in their getter method."""

        raw_data_set = DataParser().GermanCredit
        dataset = raw_data_set
        # dataset = self.format_data(raw_data_set)
        dataset = FeatureExtraction().apply_all(dataset)

        assert isinstance(dataset, pd.DataFrame)
        return dataset

    @property
    def TargetClass(self):
        """str: Properties should be documented in their getter method."""
        return "Predict"





if __name__ == "__main__":
    print("hello world")

