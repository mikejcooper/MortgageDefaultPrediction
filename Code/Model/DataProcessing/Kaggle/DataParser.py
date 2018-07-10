import os
import pandas as pd

class DataParser:
    """ A class that parses input data from file. """

    LENDING_CLUB_DATA_NAME = "lending_club"
    LENDING_CLUB_REDUCED_DATA_NAME = "lending_club_reduced"

    REPLICATE_LENDING_CLUB_PROCESSED_DATA_NAME = "replicate_lending_club_processed"


    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        self._ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self._DATA_DIR = "/../../../../Data/"
        # self._dataFrame = self._read_cvv('./data/lending_club.csv')
        # self._dataFrame = self._read_HDFStore(self.LENDING_CLUB_REDUCED_DATA_NAME)
        # self._dataFrameDescription = self._read_cvv(self.LENDING_CLUB_DATA_DESCRIPTION_NAME)
        # self._write_reduced_HDFStore(self.dataFrame,self.LENDING_CLUB_REDUCED_DATA_NAME,0.1)


    def _read_cvv(self, file_name):
        return pd.read_csv(self._ROOT_DIR + self._DATA_DIR + file_name + ".csv")

    def _write_HDFStore(self, df, file_name):
        backup = pd.HDFStore(self._ROOT_DIR + self._DATA_DIR + file_name + ".h5")
        backup['data'] = df

    def write_reduced_HDFStore(self, df, file_name, frac):
        df = pd.DataFrame.sample(df,frac=frac)
        backup = pd.HDFStore(self._ROOT_DIR + self._DATA_DIR + file_name + ".h5")
        backup['data'] = df

    def _read_HDFStore(self, file_name):
        backup = pd.HDFStore(self._ROOT_DIR + self._DATA_DIR + file_name + ".h5")
        return backup['data']

    @property
    def dataLendingClub(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_HDFStore(self.LENDING_CLUB_DATA_NAME)
        assert isinstance(df, pd.DataFrame)
        return df

    @property
    def dataLendingClubReduced(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_HDFStore(self.LENDING_CLUB_REDUCED_DATA_NAME)
        assert isinstance(df, pd.DataFrame)
        return df

    @property
    def replicateDataLendingClubProcessed(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_HDFStore(self.REPLICATE_LENDING_CLUB_PROCESSED_DATA_NAME)
        assert isinstance(df, pd.DataFrame)
        return df





if __name__ == "__main__":
    DataParser()

