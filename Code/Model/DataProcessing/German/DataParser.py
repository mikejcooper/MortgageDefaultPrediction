import os
import pandas as pd

class DataParser:
    """ A class that parses input data from file. """

    GERMAN_CREDIT_DATA_NAME = "german"

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        self._ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self._DATA_DIR = "/../../../../Data/"


    def _read_txt(self, file_name):
        file = self._ROOT_DIR + self._DATA_DIR + file_name + ".data.txt"
        return pd.read_table(file, delim_whitespace=True,
                                   names=["Status", "Month", "Credit", "Purpose",
                                          "CreditAMT",
                                          "Savings", "Employment", "Installment",
                                          "SexMarital", "Position", "Residence",
                                          "Property", "Age", "OtherInstallment",
                                          "Housing", "ExistCredits", "Job",
                                          "Liability", "Phone", "Foreign", "Predict"])

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
    def GermanCredit(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt(self.GERMAN_CREDIT_DATA_NAME)
        assert isinstance(df, pd.DataFrame)
        return df





if __name__ == "__main__":
    DataParser()

