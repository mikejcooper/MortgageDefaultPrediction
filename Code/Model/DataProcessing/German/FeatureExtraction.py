import pandas as pd
import numpy as np
from skmultilearn.problem_transform import LabelPowerset


class FeatureExtraction:
    """ A class that parses input data from file. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        # self._dataFrame = data_frame
        # assert isinstance(self._dataFrame, pd.DataFrame)
        # print self._dataFrame.dtypes

        # self.ml_model(data_frame)

    def apply_all(self, df):
        df = self.map_english_column_names(df)
        df = self.one_hot_encoder(df, exceptions=['Predict'])
        # df['Predict'] = LabelPowerset().transform(df['Predict'])

        return df

    def remove_null_values(self, df):
        """Remove column from dataset if the number of null values is greater than X. """
        assert isinstance(df, pd.DataFrame)

        for column in df:
            numberOfNulls = df[column].isnull().sum()
            lengthOfColumn = len(df[column])
            if numberOfNulls > lengthOfColumn / 4:
                df.drop([column], axis=1, inplace=True)

        return df

    def remove_columns(self, df, columns):
        df.drop(columns, axis=1, inplace=True)
        return df

    def remove_non_numerical_cats(self, df):
        for column in df:
            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype, np.dtype(int).type):
                df = self.remove_columns(df, column)
        return df

    def one_hot_encoder(self, df, exceptions=None):

        for column in df:
            if column in exceptions:
                continue

            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype, np.dtype(int).type):
                df = pd.get_dummies(df, columns=[column])
        return df

    def numerical_value_encoder(self, df_credit):
        print("Purpose : ", df_credit.Purpose.unique())
        print("Sex : ", df_credit.Sex.unique())
        print("Housing : ", df_credit.Housing.unique())
        print("Saving accounts : ", df_credit['Saving accounts'].unique())
        print("Risk : ", df_credit['Risk'].unique())
        print("Checking account : ", df_credit['Checking account'].unique())
        print("Aget_cat : ", df_credit['Age_cat'].unique())

        df_credit.Purpose.replace(('radio/TV', 'education', 'furniture/equipment', 'car', 'business',
                                   'domestic appliances', 'repairs', 'vacation/others'), (0, 1, 2, 3, 4, 5, 6, 7),
                                  inplace=True)

        df_credit.Sex.replace(('female', 'male'), (0, 1), inplace=True)

        df_credit.Housing.replace(('own', 'free', 'rent'), (0, 1, 2), inplace=True)

        df_credit["Saving accounts"].replace((str('nan'), 'little', 'quite rich', 'rich', 'moderate'), (0, 1, 3, 4, 2),
                                             inplace=True)

        df_credit.Risk.replace(('good', 'bad'), (0, 1), inplace=True)

        df_credit["Checking account"].replace(('little', 'moderate', 'rich'), (0, 1, 2), inplace=True)

        df_credit["Age_cat"].replace(('Student', 'Young', 'Adult', 'Senior'), (0, 1, 2, 3), inplace=True)

        # for column in df:
        #     if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype, np.dtype(int).type):
        #         catagories = df[column].dropna().unique()
        #         print(catagories)
        #         values = range(0,len(catagories))
        #         df.Purpose.replace(catagories, values, inplace=True)



    def map_english_column_names(self, df):
        map = {
            "A11": "0 DM",
            "A12": "< 200 DM",
            "A14": ">= 200 DM",
            "A14": "No checking acount",
            "A30": "no credits taken/all credits paid back duly",
            "A31": "all credits at this bank paid back duly",
            "A32": "existing credits paid back duly till now",
            "A33": "delay in paying off in the past",
            "A34": "critical account/other credits existing (not at this bank)",
            "A40": "car (new)",
            "A41": "car (used)",
            "A42": "furniture/equipment",
            "A43": "radio/television",
            "A44": "domestic appliances",
            "A45": "repairs",
            "A46": "education",
            "A47": "(vacation - does not exist?)",
            "A48": "retraining",
            "A49": "business",
            "A410": "others",
            "A61": "X < 100 DM",
            "A62": "100 <= X <  500 DM",
            "A63": "500 <= X < 1000 DM",
            "A64": "X >= 1000 DM",
            "A65": "unknown/ no savings account",
            "A71": "unemployed",
            "A72": "X < 1 year",
            "A73": "1 <= X < 4 years",
            "A74": "4 <= X < 7 years",
            "A75": "X >= 7 years",
            "A91": "male divorced/separated",
            "A92": "female divorced/separated/married",
            "A93": "male single",
            "A94": "male married/widowed",
            "A95": "female single",
            "A101": "none",
            "A102": "co-applicant",
            "A103": "guarantor",
            "A121": "real estate",
            "A122": "building society savings agreement/life insurance",
            "A123": "car or other",
            "A124": "unknown / no property",
            "A141": "bank",
            "A142": "stores",
            "A143": "none",
            "A151": "rent",
            "A152": "own",
            "A153": "for free",
            "A171": "unemployed/ unskilled  - non-resident",
            "A172": "unskilled - resident",
            "A173": "skilled employee / official",
            "A174": "management/ self-employed/highly qualified employee/ officer",
            "A191": "none",
            "A192": "yes, registered under the customers name",
            "A201": "yes",
            "A202": "no"}

        for column in df:
            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype,
                                                                                               np.dtype(int).type):
                df[column] = df[column].map(map)

        return df





if __name__ == "__main__":

    print("hello world")

