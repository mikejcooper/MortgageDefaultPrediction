import os
from random import sample

import pandas as pd

import DataProcessing.American.Globals as Globals

from DataProcessing.German.DataProcessing import DataProcessing as GermanDataProcessing
from DataProcessing.Kaggle.DataProcessing import DataProcessing as KaggleDataProcessing
from DataProcessing.American.DataProcessing import DataProcessing as AmericanDataProcessing




class DataGenerator:
    """ A class that parses input data from file. """

    @property
    def ActiveDataset(self):
        """str: Properties should be documented in their getter method."""

        if Globals.GERMAN_DATA:
            data = GermanDataProcessing().Dataset
        elif Globals.KAGGLE_DATA:
            data = KaggleDataProcessing().Dataset
        elif Globals.AMERICAN_DATA:
            data = AmericanDataProcessing().Dataset
        else:
            raise ValueError('No dataset selected')

        assert isinstance(data, pd.DataFrame)
        return data

    def ActiveDataset_i(self, i):
        """str: Properties should be documented in their getter method."""

        if Globals.GERMAN_DATA:
            data = GermanDataProcessing().Dataset
        elif Globals.KAGGLE_DATA:
            data = KaggleDataProcessing().Dataset
        elif Globals.AMERICAN_DATA:
            # data = AmericanDataProcessing().Dataset_Origin()
            # data = data[:50000]

            data = AmericanDataProcessing().Dataset_Combo_i(i)
            # data = AmericanDataProcessing().Dataset_Combo_i(i)
        else:
            raise ValueError('No dataset selected')

        assert isinstance(data, pd.DataFrame)
        return data

    @property
    def Number_Of_Datasets(self):
        """str: Properties should be documented in their getter method."""

        if Globals.GERMAN_DATA:
            number = 1
        elif Globals.KAGGLE_DATA:
            number = 1
        elif Globals.AMERICAN_DATA:
            number = AmericanDataProcessing().Dataset_count
        else:
            raise ValueError('No dataset selected')

        return number


    @property
    def ActiveTargetClass(self):
        if Globals.GERMAN_DATA:
            target_class = GermanDataProcessing().TargetClass
        elif Globals.KAGGLE_DATA:
            target_class = KaggleDataProcessing().TargetClass
        elif Globals.AMERICAN_DATA:
            target_class = AmericanDataProcessing().TargetClass
        else:
            raise ValueError('No target class selected')

        # assert isinstance(target_class, )
        return target_class




if __name__ == "__main__":
    print("hello world")

