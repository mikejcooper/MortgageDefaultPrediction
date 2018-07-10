import os

import math
import platform

import pandas as pd
import numpy as np

class DataParser:
    """ A class that parses input data from file. """

    SAMPLE_1999_ORIGINATION = "sample_1999/sample_orig_1999"
    SAMPLE_1999_MONTHLY = "sample_1999/sample_svcg_1999"

    DATA_1999_Q1_ORIGINATION = "historical_data1_Q11999/historical_data1_Q11999"
    DATA_1999_Q1_MONTHLY = "historical_data1_Q11999/historical_data1_time_Q11999"

    COMBO_BLUEP4_FE2 = True

    # _FE2 = FE1 completed
    # _FE2_Filtered = FE2 completed



    VALID_DATA = [
        ["1999", ["Q1", "Q2", "Q3", "Q4"]],
        ["2000", ["Q1", "Q2", "Q3", "Q4"]],
        ["2002", ["Q1", "Q2", "Q3", "Q4"]],
        ["2003", ["Q1", "Q2", "Q3", "Q4"]],
        ["2004", ["Q1", "Q2", "Q3", "Q4"]],
        ["2005", ["Q1", "Q2", "Q3", "Q4"]],
        ["2006", ["Q1", "Q2", "Q3", "Q4"]],
        ["2007", ["Q1", "Q2", "Q3", "Q4"]],
        ["2008", ["Q1", "Q2", "Q3", "Q4"]],
        ["2009", ["Q1", "Q2", "Q3", "Q4"]],
        ["2010", ["Q1", "Q2", "Q3", "Q4"]],
        ["2011", ["Q1", "Q2", "Q3", "Q4"]],
        ["2012", ["Q1", "Q2", "Q3", "Q4"]],
        ["2013", ["Q1", "Q2", "Q3", "Q4"]],
        ["2014", ["Q1", "Q2", "Q3", "Q4"]],
        ["2015", ["Q1", "Q2", "Q3", "Q4"]],
        ["2016", ["Q1", "Q2"]],
    ]

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        self._ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self._DATA_DIR = "/../../../../Data/American/"
        if platform.system() != 'Darwin':
            self._ROOT_DIR = '/mnt/storage/scratch/mc14641/data/'
            self._DATA_DIR = ""

        self.origination_names = ['fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts',
                                 'cltv' ,'dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st',
                                 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name',
                                 'servicer_name', 'flag_sc']

        self.monthly_names = ['id_loan', 'svcg_cycle', 'current_upb', 'delq_sts', 'loan_age', 'mths_remng',
                              'repch_flag', 'flag_mod',
                              'cd_zero_bal', 'dt_zero_bal', 'current_int_rt', 'non_int_brng_upb', 'dt_lst_pi',
                              'mi_recoveries',
                              'net_sale_proceeds', 'non_mi_recoveries', 'expenses', 'legal_costs', 'maint_pres_costs',
                              'taxes_ins_costs', 'misc_costs', 'actual_loss', 'modcost']

 # self.monthly_names_ordered = ['delq_sts', 'dt_zero_bal', 'current_int_rt', 'current_upb', 'dt_lst_pi', 'mi_recoveries',
        #                       'net_sale_proceeds', 'non_mi_recoveries', 'expenses', 'legal_costs', 'maint_pres_costs',
        #                       'taxes_ins_costs', 'misc_costs', 'actual_loss', 'modcost',
        #                       'id_loan', 'mths_remng', 'svcg_cycle', 'loan_age', 'repch_flag', 'flag_mod',
        #                       'cd_zero_bal', 'non_int_brng_upb']

    def _read_txt_monthly(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_monthly_path(i)
        return pd.read_table(path + ".txt",  sep='|', names=self.monthly_names)

    def _read_txt_origination(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_origination_path(i)
        return pd.read_table(path + ".txt",  sep='|', names=self.origination_names)

    def _read_txt(self, file_name, names):
        path = self._ROOT_DIR + self._DATA_DIR + file_name
        return pd.read_table(path + ".txt",  sep='|', names=names)

    def _read_cvv(self, file_name):
        return pd.read_csv(self._ROOT_DIR + self._DATA_DIR + file_name + ".csv")

    def _write_HDFStore_Combined_FE2(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i)
        if platform.system() != 'Darwin' and self.COMBO_BLUEP4_FE2:
            path = path + "_FE2_Filtered"
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        chunk_size = 6

        backup = pd.HDFStore(path + ".h5")
        backup['chunk_size'] = pd.DataFrame([chunk_size])
        backup.close()

        df_chunks = self.chunk_df(df, chunk_size)
        for i in range(0, chunk_size):
            backup = pd.HDFStore(path + ".h5")
            backup['data_' + str(i)] = df_chunks[i]
            backup.close()

    def _write_HDFStore_Combined_FE(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i)
        if platform.system() != 'Darwin' and self.COMBO_BLUEP4_FE2:
            path = path + "_FE2"
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        chunk_size = 6

        backup = pd.HDFStore(path + ".h5")
        backup['chunk_size'] = pd.DataFrame([chunk_size])
        backup.close()

        df_chunks = self.chunk_df(df, chunk_size)
        for i in range(0, chunk_size):
            backup = pd.HDFStore(path + ".h5")
            backup['data_' + str(i)] = df_chunks[i]
            backup.close()

    def _write_HDFStore_OHE(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i) + "OHE"
        if platform.system() != 'Darwin' and self.COMBO_BLUEP4_FE2:
            path = path + "_OHC"
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        chunk_size = 6

        backup = pd.HDFStore(path + ".h5")
        backup['chunk_size'] = pd.DataFrame([chunk_size])
        backup.close()

        df_chunks = self.chunk_df(df, chunk_size)
        for i in range(0, chunk_size):
            backup = pd.HDFStore(path + ".h5")
            backup['data_' + str(i)] = df_chunks[i]
            backup.close()



    def _write_HDFStore_Origination(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_origination_path(i)
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = df
        backup.close()

    def _write_HDFStore_Origination_Filtered(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_origination_filtered_path(i)
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = df
        backup.close()

    def _write_HDFStore_Monthly(self, df, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_monthly_path(i)
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = pd.DataFrame()
        os.remove(path + ".h5")
        backup = pd.HDFStore(path + ".h5")
        backup['data'] = df
        backup.close()

    def _read_HDFStore_Combined_FE2(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i)
        if platform.system() != 'Darwin' and self.COMBO_BLUEP4_FE2:
            path = path + "_FE2_Filtered"
        backup = pd.HDFStore(path + ".h5")
        if 'chunk_size' in backup:
            chunk_size = backup['chunk_size'][0][0]
            df = pd.DataFrame()
            for i in range(0, chunk_size):
                data = backup['data_' + str(i)]
                df = pd.concat([df, data], axis=0)
        else :
            df = backup['data']
        backup.close()
        return df

    def _read_HDFStore_Combined_FE(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i)
        if platform.system() != 'Darwin' and self.COMBO_BLUEP4_FE2:
            path = path + "_FE2"
        backup = pd.HDFStore(path + ".h5")
        if 'chunk_size' in backup:
            chunk_size = backup['chunk_size'][0][0]
            df = pd.DataFrame()
            for i in range(0, chunk_size):
                data = backup['data_' + str(i)]
                df = pd.concat([df, data], axis=0)
        else :
            df = backup['data']
        backup.close()
        return df

    def _read_HDFStore_OHE(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_combo_path(i) + "OHE"
        if platform.system() != 'Darwin':
            path += "_OHC"

        backup = pd.HDFStore(path + ".h5")
        if 'chunk_size' in backup:
            chunk_size = backup['chunk_size'][0][0]
            df = pd.DataFrame()
            for i in range(0, chunk_size):
                data = backup['data_' + str(i)]
                df = pd.concat([df, data], axis=0)
        else :
            df = backup['data']
        backup.close()
        return df

    def _read_HDFStore_Origination(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_origination_path(i)
        backup = pd.HDFStore(path + ".h5")
        data = backup['data']
        backup.close()
        return data

    def _read_HDFStore_Origination_Filtered(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_origination_filtered_path(i)
        backup = pd.HDFStore(path + ".h5")
        data = backup['data']
        backup.close()
        return data

    def _read_HDFStore_Monthly(self, i):
        path = self._ROOT_DIR + self._DATA_DIR + self._get_monthly_path(i)
        backup = pd.HDFStore(path + ".h5")
        data = backup['data']
        backup.close()
        return data

    @property
    def AmericanCredit(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt(self.SAMPLE_1999_ORIGINATION, self.origination_names)
        assert isinstance(df, pd.DataFrame)
        return df

    @property
    def AmericanOrigination(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt(self.SAMPLE_1999_ORIGINATION, self.origination_names)
        assert isinstance(df, pd.DataFrame)
        return df

    @property
    def AmericanMonthly(self):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt(self.SAMPLE_1999_MONTHLY, self.monthly_names)
        assert isinstance(df, pd.DataFrame)
        return df

    def AmericanCombo_i_FE(self, i):
        """str: Properties should be documented in their getter method."""
        df = self._read_HDFStore_Combined_FE(i)
        assert isinstance(df, pd.DataFrame)
        return df

    def AmericanCombo_i_FE2(self, i):
        """str: Properties should be documented in their getter method."""
        df = self._read_HDFStore_Combined_FE2(i)
        assert isinstance(df, pd.DataFrame)
        return df

    def AmericanOrigination_i(self, i):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt_origination(i)
        # df = self._read_HDFStore_Origination(i)
        assert isinstance(df, pd.DataFrame)
        return df

    def AmericanMonthly_i(self, i):
        """str: Properties should be documented in their getter method."""
        df = self._read_txt_monthly(i)
        # df = self._read_HDFStore_Monthly(i)
        assert isinstance(df, pd.DataFrame)
        return df

    @property
    def number_of_datasets(self):
        """str: Properties should be documented in their getter method."""
        return sum([len(year[1]) for year in self.VALID_DATA ])

    @property
    def number_of_years(self):
        """str: Properties should be documented in their getter method."""
        return len(self.VALID_DATA)

    def national_mortgage_rate(self):
        path = self._ROOT_DIR + "/Additional_Data/mortgage_rate"
        if platform.system() != 'Darwin':
            path = "/mnt/storage/home/mc14641/Thesis/Code/Model/DataProcessing/American/Additional_Data/mortgage_rate"
        return pd.read_table(path + ".csv", sep=',', names=['svcg_cycle', 'nat_int_rt'])

    def national_housing_price_index(self):
        path = self._ROOT_DIR + "/Additional_Data/housing_price_index"
        if platform.system() != 'Darwin':
            path = "/mnt/storage/home/mc14641/Thesis/Code/Model/DataProcessing/American/Additional_Data/housing_price_index"
        return pd.read_table(path + ".csv", sep=',', names=['svcg_cycle', 'hous_prc_indx_st', 'st'])

    def national_unemploy_rt(self):
        path = self._ROOT_DIR + "/Additional_Data/unemployment_rates"
        if platform.system() != 'Darwin':
            path = "/mnt/storage/home/mc14641/Thesis/Code/Model/DataProcessing/American/Additional_Data/unemployment_rates"
        return pd.read_table(path + ".csv", sep=',', names=['svcg_cycle', 'st', 'unemploy_rt'])

    def st_names(self):
        path = self._ROOT_DIR + "/Additional_Data/st_names"
        if platform.system() != 'Darwin':
            path = "/mnt/storage/home/mc14641/Thesis/Code/Model/DataProcessing/American/Additional_Data/unemployment_rates"
        return pd.read_table(path + ".csv", sep=',', names=['st', 'st_name'])


    def _get_file_info_i(self, i):
        data_year = None
        data_Qi = None
        i_count = 0
        done = False
        for year in self.VALID_DATA:
            for Qi in year[1]:
                if i_count == i:
                    data_year = year[0]
                    data_Qi = Qi
                    done = True
                    break
                i_count += 1
            if done:
                break

        print (data_year, data_Qi)
        return (data_year, data_Qi)


    def _get_monthly_path(self, i):
        (data_year, data_Qi) = self._get_file_info_i(i)
        folder = "historical_data1_" + data_year + "/" + "historical_data1_" + data_Qi + data_year + "/"
        file_monthly = "historical_data1_time_" + data_Qi + data_year
        return folder + file_monthly

    def _get_origination_path(self, i):
        (data_year, data_Qi) = self._get_file_info_i(i)
        folder = "historical_data1_" + data_year + "/" + "historical_data1_" + data_Qi + data_year + "/"
        file_origin = "historical_data1_" + data_Qi + data_year
        return folder + file_origin

    def _get_origination_filtered_path(self, i):
        if i < 0:
            return "other/file" + str(i)
        (data_year, data_Qi) = self._get_file_info_i(i)
        folder = "historical_data1_" + data_year + "/" + "historical_data1_" + data_Qi + data_year + "/"
        file_origin = "historical_data_origination_filtered_" + data_Qi + data_year
        return folder + file_origin

    def _get_combo_path(self, i):
        if i == -1:
            return  "other/big_data"
        if i == -2:
            return  "other/big_data_tmp"
        if i == -3:
            return  "other/big_data_bigger"
        if i == -4:
            return  "other/unbalanced"
        if i == -5:
            return  "other/npl"
        (data_year, data_Qi) = self._get_file_info_i(i)
        folder = "historical_data1_" + data_year + "/" + "historical_data1_" + data_Qi + data_year + "/"
        file_origin = "historical_data1_" + data_Qi + data_year + "Combo"
        return folder + file_origin

    def _remove_HDFStores(self):
        for i in range(0, self.number_of_datasets):
            path = self._ROOT_DIR + self._DATA_DIR + self._get_monthly_path(i) + ".h5"
            path2 = self._ROOT_DIR + self._DATA_DIR + self._get_origination_path(i) + ".h5"
            if os.path.isfile(path):
                os.remove(path)  # remove the file
            else:
                print("path not exist: " + str(i))
            if os.path.isfile(path2):
                os.remove(path2)  # remove the file
            else:
                print("path2 not exist: " + str(i))

    def chunk_df(self, df, chunk_size):
        remainder = len(df) % chunk_size
        split = len(df) - remainder
        step = split / chunk_size
        df_chunks = []
        for i in range(0, chunk_size):
            if (i == chunk_size - 1):
                df_chunks.append(df[i*step: (i+1)*step + remainder])
            else:
                df_chunks.append(df[i*step: (i+1)*step])
        return df_chunks




if __name__ == "__main__":
    DataParser().AmericanOrigination_i(5)
    DataParser().AmericanMonthly_i(5)

