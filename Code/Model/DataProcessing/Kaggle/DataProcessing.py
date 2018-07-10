import pandas as pd

from DataParser import DataParser
import FeatureExtraction


class DataProcessing:
    """ A class that pre-processes data"""

    def __init__(self):
        """ Example of docstring on the __init__ method.  """

    @property
    def Dataset(self):
        """str: Properties should be documented in their getter method."""

        # raw_data_set = DataParser().GermanCredit
        # dataset = FeatureExtraction().apply_all(raw_data_set)

        dataset = DataParser().replicateDataLendingClubProcessed

        assert isinstance(dataset, pd.DataFrame)
        return dataset

    @property
    def TargetClass(self):
        """str: Properties should be documented in their getter method."""
        return "loan_status_encoded"





if __name__ == "__main__":
    print("hello world")

