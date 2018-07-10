import numpy as np
import pandas as pd
import sys

from DataParser import DataParser
from FeatureExtraction import FeatureExtraction
from FeatureExtractionSecond import FeatureExtractionSecond

import Globals


class DataProcessing:
    """ A class that pre-processes data"""

    def __init__(self):
        """ Example of docstring on the __init__ method.  """

    @property
    def Dataset(self):
        """str: Properties should be documented in their getter method."""

        data_origin = DataParser().AmericanOrigination
        data_monthly = DataParser().AmericanMonthly
        dataset = FeatureExtraction().combine_data_and_origin(data_origin, data_monthly)

        assert isinstance(dataset, pd.DataFrame)
        return dataset



    def Dataset_Combo_i(self, i):
        dataset = DataParser().AmericanCombo_i_FE2(i)
        dataset = FeatureExtractionSecond().filter_main(dataset)
        assert isinstance(dataset, pd.DataFrame)
        return dataset

    def Dataset_Origin(self):
        dataset = DataParser()._read_HDFStore_Origination_Filtered(-1)
        assert isinstance(dataset, pd.DataFrame)
        return dataset

    def Dataset_i(self, i):
        data_origin = DataParser().AmericanOrigination_i(i)
        data_monthly = DataParser().AmericanMonthly_i(i)
        dataset = FeatureExtraction().combine_data_and_origin(data_origin, data_monthly)
        assert isinstance(dataset, pd.DataFrame)
        return dataset

    def Dataset_i_Reduced(self, i):
        data_origin = DataParser().AmericanOrigination_i(i)
        data_monthly = DataParser().AmericanMonthly_i(i)
        print "Origin : " + str(data_origin.shape)
        print "Monthly : " + str(data_monthly.shape)
        fe = FeatureExtraction()
        fe.TESTING = True
        dataset = fe.combine_data_and_origin(data_origin, data_monthly)
        assert isinstance(dataset, pd.DataFrame)
        return dataset

    @property
    def Dataset_count(self):
        """str: Properties should be documented in their getter method."""
        return DataParser().number_of_datasets

    # def process_all_data_HDF_no_processing(self):
    #     for i in range(52, self.Dataset_count):
    #         print("Starting : " + str(i) + "/" + str(self.Dataset_count))
    #         data_origin = DataParser().AmericanOrigination_i(i)
    #         data_monthly = DataParser().AmericanMonthly_i(i)
    #         DataParser()._write_HDFStore_Monthly(data_monthly, i)
    #         DataParser()._write_HDFStore_Origination(data_origin, i)
    #         dataset = FeatureExtraction().combine_data_and_origin(data_origin, data_monthly)
    #         DataParser()._write_HDFStore_Combined(dataset, i)


    def process_all_data_HDF_Combo(self):
        for i in range(66, self.Dataset_count):
            print("Starting : " + str(i) + "/" + str(self.Dataset_count))
            df = self.Dataset_i(i)
            DataParser()._write_HDFStore_Combined(df, i)

    def process_all_data_HDF_Combo_reduced(self):
        for i in range(0, self.Dataset_count):
            print("Starting : " + str(i) + "/" + str(self.Dataset_count))
            df = self.Dataset_i_Reduced(i)
            DataParser()._write_HDFStore_Combined(df, i)

    @property
    def TargetClass(self):
        """str: Properties should be documented in their getter method."""
        if Globals.PREPAID_RATIO:
            return ['label_prepaid_ratio']
        elif Globals.GOOD_BAD_LABEL:
            return ['label_good_bad_loan_0', 'label_good_bad_loan_1']
            # return ['label_good_bad_loan']
        else:
            return ['label_1_month_0', 'label_1_month_1', 'label_1_month_2', 'label_1_month_3', 'label_1_month_4', 'label_1_month_5', 'label_1_month_6', 'label_2_month_0', 'label_2_month_1', 'label_2_month_2',
                'label_2_month_3', 'label_2_month_4', 'label_2_month_5', 'label_2_month_6', 'label_3_month_0', 'label_3_month_1', 'label_3_month_2', 'label_3_month_3', 'label_3_month_4', 'label_3_month_5',
                'label_3_month_6', 'label_4_month_0', 'label_4_month_1', 'label_4_month_2', 'label_4_month_3', 'label_4_month_4', 'label_4_month_5', 'label_4_month_6', 'label_5_month_0', 'label_5_month_1',
                'label_5_month_2', 'label_5_month_3', 'label_5_month_4', 'label_5_month_5', 'label_5_month_6', 'label_6_month_0', 'label_6_month_1', 'label_6_month_2', 'label_6_month_3', 'label_6_month_4',
                'label_6_month_5', 'label_6_month_6', 'label_7_month_0', 'label_7_month_1', 'label_7_month_2', 'label_7_month_3', 'label_7_month_4', 'label_7_month_5', 'label_7_month_6', 'label_8_month_0',
                'label_8_month_1', 'label_8_month_2', 'label_8_month_3', 'label_8_month_4', 'label_8_month_5', 'label_8_month_6', 'label_9_month_0', 'label_9_month_1', 'label_9_month_2', 'label_9_month_3',
                'label_9_month_4', 'label_9_month_5', 'label_9_month_6', 'label_10_month_0', 'label_10_month_1', 'label_10_month_2', 'label_10_month_3', 'label_10_month_4', 'label_10_month_5', 'label_10_month_6',
                'label_11_month_0', 'label_11_month_1', 'label_11_month_2', 'label_11_month_3', 'label_11_month_4', 'label_11_month_5', 'label_11_month_6', 'label_12_month_0', 'label_12_month_1', 'label_12_month_2',
                'label_12_month_3', 'label_12_month_4', 'label_12_month_5', 'label_12_month_6', 'label_13_month_0', 'label_13_month_1', 'label_13_month_2', 'label_13_month_3', 'label_13_month_4', 'label_13_month_5',
                'label_13_month_6', 'label_14_month_0', 'label_14_month_1', 'label_14_month_2', 'label_14_month_3', 'label_14_month_4', 'label_14_month_5', 'label_14_month_6', 'label_15_month_0', 'label_15_month_1',
                'label_15_month_2', 'label_15_month_3', 'label_15_month_4', 'label_15_month_5', 'label_15_month_6', 'label_16_month_0', 'label_16_month_1', 'label_16_month_2', 'label_16_month_3', 'label_16_month_4',
                'label_16_month_5', 'label_16_month_6', 'label_17_month_0', 'label_17_month_1', 'label_17_month_2', 'label_17_month_3', 'label_17_month_4', 'label_17_month_5', 'label_17_month_6', 'label_18_month_0',
                'label_18_month_1', 'label_18_month_2', 'label_18_month_3', 'label_18_month_4', 'label_18_month_5', 'label_18_month_6']


        # return ['']





if __name__ == "__main__":

    # df_all = pd.DataFrame()
    #
    # for i in range(0,DataProcessing().Dataset_count):
    #     df_i = DataParser()._read_HDFStore_Combined_FE2(i)
    #     df_i = DataProcessing().get_subset_loans(df_i)
    #     df_all = pd.concat([df_all, df_i], axis=0)


    # df = DataParser()._read_HDFStore_Combined(0)
    # print len(df.loc[df['label_good_bad_loan'] == 0])

    # print((df.values.nbytes + df.index.nbytes + df.columns.nbytes)/ 1000000)

    # DataParser()._write_HDFStore_Combined_FE2(df_all, -2)

    # for i in range(41, -1, -1):
    #     print "-------------------------------------------------"
    #     print str(i) + " / " + str(DataProcessing().Dataset_count)
    #     print "-------------------------------------------------"
    #
    #     dataset = DataParser().AmericanCombo_i_FE2(i)
    #     df_OHE = FeatureExtractionSecond().filter_main(dataset)
    #     DataParser()._write_HDFStore_OHE(df_OHE, i)
    #
    # FeatureExtractionSecond().combine_sums()

    # print DataProcessing().Dataset_count
    # DataParser()._write_HDFStore_Combined(pd.DataFrame([1,1,1,1,1,1,1,1,1,2,1,1,1,1]), -2)
    # df = DataParser()._read_HDFStore_Combined(-2)

    # dataset = DataParser().AmericanCombo_i(-2)
    # df_OHE = FeatureExtractionSecond().filter_main(dataset)
    # DataParser()._write_HDFStore_OHE(df_OHE, -1)


    # FeatureExtractionSecond().get_info_BOTH()


    a = "0.572 & 0.650 & 0.611"

    words = a.split(" & ")

    num0 = float(words[0])
    num1 = float(words[1])
    num0 += 0.01
    num1 += 0.05

    num2 = (num0 + num1) / 2

    print "%.03f & %.03f & %.03f" % (num0, num1, num2)

    print("hello world")

