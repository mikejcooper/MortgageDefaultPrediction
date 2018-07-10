import pandas as pd
import numpy as np

from Replicate import FeatureIndex
from Replicate.FeatureEngineering import trim_features
from Replicate.OneHotEncoding import one_hot_encoder
from Replicate.TrimData import drop_null_columns, split_loan_in_progress, categorize_target

class FeatureExtraction:
    """ A class that parses input data from file. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        # self._dataFrame = data_frame
        # assert isinstance(self._dataFrame, pd.DataFrame)
        # print self._dataFrame.dtypes

        # self.ml_model(data_frame)

    def apply_all(self, df):
        df = self.remove_null_values(df)
        df = self.remove_in_progress_loans(df)
        df = self.encode_loan_status(df)
        df = self.remove_columns(df, ['url'])
        df = self.remove_non_numerical_cats(df)
        return df

    def apply_all_replicate(self, df):
        # pre-process data
        drop_null_columns(df)
        loan_in_progress = split_loan_in_progress(df)
        df = categorize_target(df)
        # Feature Engineering by EDA
        trim_features(df)
        df = df[FeatureIndex.features]
        df_one_hot_encoded = one_hot_encoder(df)
        return df_one_hot_encoded

    def remove_null_values(self, df):
        """Remove column from dataset if the number of null values is greater than X. """
        assert isinstance(df, pd.DataFrame)

        for column in df:
            numberOfNulls = df[column].isnull().sum()
            lengthOfColumn = len(df[column])
            if numberOfNulls > lengthOfColumn / 4:
                df.drop([column], axis=1, inplace=True)

        return df

    def remove_in_progress_loans(self, df):
        in_progress_loan_status = ['Current', 'Issues']
        progress_bool = df.loan_status.isin(in_progress_loan_status)
        in_progress_loans = df[progress_bool].drop('loan_status', axis=1)
        df.drop(list(in_progress_loans.index), axis=0, inplace=True)
        return df

    def encode_loan_status(self, df):
        """Returns encoded loan status: Safe, Warning and Bad"""

        def func(x):
            bad_index = ['Charged Off',
                         'Does not meet the credit policy. Status:Charged Off',
                         'Default'
                         ]
            warning_index = ['Late (31-120 days)',
                             'Late (16-30 days)',
                             'In Grace Period'
                             ]
            safe_index = ['Fully Paid',
                          'Does not meet the credit policy. Status:Fully Paid'
                          ]
            if x['loan_status'] in bad_index:
                return 0
            elif x['loan_status'] in warning_index:
                return 1
            else:
                return 2

        df['loan_status_encoded'] = df.apply(func, axis=1)
        df.drop('loan_status', axis=1, inplace=True)
        return df

    def remove_columns(self, df, columns):
        df.drop(columns, axis=1, inplace=True)
        return df

    def remove_non_numerical_cats(self, df):
        for column in df:
            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype,
                                                                                               np.dtype(int).type):
                df = self.remove_columns(df, column)
        return df


if __name__ == "__main__":

    print("hello world")

