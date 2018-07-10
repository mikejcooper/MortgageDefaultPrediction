import pandas as pd
import numpy as np
import resource
import gc
import time

from DataParser import DataParser
# from DataProcessing import DataProcessing
from FeatureExtraction import FeatureExtraction
import Globals


class FeatureExtractionSecond:
    """ A class that parses input data from file. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        # self._dataFrame = data_frame
        # assert isinstance(self._dataFrame, pd.DataFrame)
        # print self._dataFrame.dtypes

        # self.ml_model(data_frame)



    def filter_main(self, data):
        start_time = time.time()

        # # -----------------------------------------------------------------------------------------
        # # Select information from loan origination date only, remove monthly updates.
        # df1 = data.sort_values("svcg_cycle", ascending=True)
        # df_unique_loan_id = df1['id_loan'].drop_duplicates().index
        # start_loans = df1.loc[df_unique_loan_id]
        # data = start_loans
        # # -----------------------------------------------------------------------------------------


        print "Filtering main"
        columns_to_remove_origination = [['repch_flag', 'flag_mod', 'flag_sc']]
        columns_to_remove_monthly = ['modcost', 'actual_loss', 'misc_costs', 'taxes_ins_costs', 'maint_pres_costs',
                                     'legal_costs', 'expenses', 'non_mi_recoveries',
                                     'net_sale_proceeds', 'mi_recoveries', 'dt_lst_pi', 'non_int_brng_upb',
                                     'dt_zero_bal', 'cd_zero_bal', 'delq_sts']
        columns = columns_to_remove_monthly + columns_to_remove_origination
        labels = [column_name for column_name in columns if "label" in column_name]
        for column in columns:
            if column not in labels:
                data = data.drop(column, 1)

        data = data.drop('id_loan', 1)
        data = data.drop('zipcode', 1)
        # data = data.drop('svcg_cycle', 1)

        data = self.prepare_labels(data)

        print("--- prepare_labels: %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        data = self.create_ohc(data)
        print("--- create_ohc: %s seconds ---" % (time.time() - start_time))
        start_time = time.time()


        columns = data.columns.values
        labels = [column_name for column_name in columns if "label" in column_name]

        columns = ['channel_B', 'channel_C', 'channel_R', 'channel_T', 'channel_U', 'flag_fthb_N',
                   'flag_fthb_U', 'flag_fthb_Y', 'loan_purpose_C', 'loan_purpose_L',
                   'loan_purpose_N', 'loan_purpose_U', 'occpy_sts_I', 'occpy_sts_O',
                   'occpy_sts_S', 'occpy_sts_U', 'ppmt_pnlty_N', 'ppmt_pnlty_U', 'ppmt_pnlty_Y',
                   'prod_type_FRM', 'prod_type_U', 'prop_type_CO', 'prop_type_CP',
                   'prop_type_LH', 'prop_type_MH', 'prop_type_PU', 'prop_type_SF', 'prop_type_U',
                   'st_AK', 'st_AL', 'st_AR', 'st_AZ', 'st_CA', 'st_CO', 'st_CT', 'st_DC', 'st_DE',
                   'st_FL', 'st_GA', 'st_HI', 'st_IA', 'st_ID', 'st_IL', 'st_IN', 'st_KS', 'st_KY',
                   'st_LA', 'st_MA', 'st_MD', 'st_ME', 'st_MI', 'st_MN', 'st_MO', 'st_MS', 'st_MT',
                   'st_NC', 'st_ND', 'st_NE', 'st_NH', 'st_NJ', 'st_NM', 'st_NV', 'st_NY', 'st_OH',
                   'st_OK', 'st_OR', 'st_PA', 'st_RI', 'st_SC', 'st_SD', 'st_TN', 'st_TX', 'st_UT',
                   'st_VA', 'st_VT', 'st_WA', 'st_WI', 'st_WV', 'st_WY', 'svcg_cycle',
                   'occr_default_per_state', 'occr_default_per_state_12_mon',
                   'occr_paid_off_per_state', 'occr_paid_off_per_state_12_mon',
                   'new_loans_per_state_12_mon', 'new_loans_per_state', 'active_loans_per_state',
                   'occr_default_per_zipcode', 'occr_default_per_zipcode_12_mon',
                   'occr_paid_off_per_zipcode', 'occr_paid_off_per_zipcode_12_mon',
                   'new_loans_per_zipcode_12_mon', 'new_loans_per_zipcode', 'active_loans_per_zipcode', 'nat_int_rt',
                   'unemploy_rt', 'hous_prc_indx_st', 'fico',
                   'dt_first_pi', 'dt_matr', 'cd_msa', 'mi_pct', 'cnt_units', 'cltv', 'dti',
                   'orig_upb', 'ltv', 'int_rt', 'orig_loan_term', 'cnt_borr', 'current_upb',
                   'loan_age', 'mths_remng', 'current_int_rt', 'status_month_0',
                   'time_since_origin', 'pct_change', 'crt_minus_nat_int_rt',
                   'occr_crt_less_than_nat_int_rate', 'occr_curr_12_mon', 'occr_curr',
                   'occr_30dd_12_mon', 'occr_30dd', 'occr_60dd_12_mon', 'occr_60dd',
                   'occr_90dd_12_mon', 'occr_90dd', 'occr_foreclosed_12_mon', 'occr_foreclosed',
                   'tmp', 'rt_default_per_zipcode', 'rt_default_per_zipcode_12_mon',
                   'rt_default_per_state', 'rt_default_per_state_12_mon']


        # columns = ['channel_B', 'channel_C', 'channel_R', 'channel_T', 'channel_U', 'flag_fthb_N',
        #            'flag_fthb_U', 'flag_fthb_Y', 'loan_purpose_C', 'loan_purpose_L',
        #            'loan_purpose_N', 'loan_purpose_U', 'occpy_sts_I', 'occpy_sts_O',
        #            'occpy_sts_S', 'occpy_sts_U', 'ppmt_pnlty_N', 'ppmt_pnlty_U', 'ppmt_pnlty_Y',
        #            'prod_type_FRM', 'prod_type_U', 'prop_type_CO', 'prop_type_CP',
        #            'prop_type_LH', 'prop_type_MH', 'prop_type_PU', 'prop_type_SF', 'prop_type_U',
        #            'st_AK', 'st_AL', 'st_AR', 'st_AZ', 'st_CA', 'st_CO', 'st_CT', 'st_DC', 'st_DE',
        #            'st_FL', 'st_GA', 'st_HI', 'st_IA', 'st_ID', 'st_IL', 'st_IN', 'st_KS', 'st_KY',
        #            'st_LA', 'st_MA', 'st_MD', 'st_ME', 'st_MI', 'st_MN', 'st_MO', 'st_MS', 'st_MT',
        #            'st_NC', 'st_ND', 'st_NE', 'st_NH', 'st_NJ', 'st_NM', 'st_NV', 'st_NY', 'st_OH',
        #            'st_OK', 'st_OR', 'st_PA', 'st_RI', 'st_SC', 'st_SD', 'st_TN', 'st_TX', 'st_UT',
        #            'st_VA', 'st_VT', 'st_WA', 'st_WI', 'st_WV', 'st_WY', 'svcg_cycle','fico',
        #            'dt_first_pi', 'dt_matr', 'cd_msa', 'mi_pct', 'cnt_units', 'cltv', 'dti',
        #            'orig_upb', 'ltv', 'int_rt', 'orig_loan_term', 'cnt_borr', 'current_upb',
        #            'loan_age', 'mths_remng', 'current_int_rt', 'status_month_0',
        #            'time_since_origin'
        #            ]

        # data['f1'] = data['label_good_bad_loan_0'].astype(float)
        # data['f1'] = data['f1'].apply(lambda x: int(x) + np.random.rand()*0.75 )
        # # data['f1'] = data['occr_30dd'].astype(float)
        # columns = ['f1']

        columns_allowed = columns + labels

        for column in data.columns.values:
            if column not in columns_allowed:
                data = data.drop(column, 1)
                print column




        print("--- end: %s seconds ---" % (time.time() - start_time))

        return data

    def create_ohc(self, data, exceptions=[]):
        d = {
            'ppmt_pnlty': ['Y', 'N', 'U'],
            'flag_fthb': ['Y', 'N', 'U'],
            'occpy_sts': ['O', 'I', 'S', 'U'],
            'channel': ['R', 'B', 'C', 'T', 'U'],
            'prod_type': ['FRM', 'U'],
            'prop_type': ['SF', 'PU', 'CO', 'MH', 'CP', 'LH', 'U'],
            'loan_purpose': ['L', 'N', 'C', 'U'],
            'st': ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN',
                   'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
                   'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA',
                   'WI', 'WV', 'WY']
        }

        d_labels = {'label_1_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_2_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_3_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_4_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_5_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_6_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_7_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_8_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_9_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_10_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_11_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_12_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_13_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_14_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_15_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_16_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_17_month': ['0', '1', '2', '3', '4', '5', '6'],
                    'label_18_month': ['0', '1', '2', '3', '4', '5', '6']
                    }

        if Globals.MULTI_LABEL:
            d = reduce(lambda x, y: dict(x, **y), (d, d_labels))

        # if Globals.GOOD_BAD_LABEL:
        #     data['label_good_bad_loan'] = data['label_good_bad_loan'].astype(int)
        #     exceptions = ['label_good_bad_loan']



        # Max all arrays in dict the same length
        max = 0
        for d_i in d:
            if len(d[d_i]) > max:
                max = len(d[d_i])
        for d_i in d:
            d[d_i] = d[d_i] + [np.nan] * (max - len(d[d_i]))

        # Create template dataframe from dictionary
        data_template = pd.DataFrame(data=d)
        data_template_ohc = self.one_hot_encoder(data_template, exceptions)

        data_ohc = self.one_hot_encoder(data, exceptions)

        # return data_ohc

        # print data_ohc.columns.values
        # print data_template_ohc.columns.values

        # Create row for each monthly update and concat with origin data
        data_ohc_all = pd.merge(data_template_ohc, data_ohc, how='right')

        # Make extra ohc vars = 0
        for column in data_template_ohc:
            data_ohc_all.loc[pd.isnull(data_ohc_all[column]), column] = 0

        return data_ohc_all

    def one_hot_encoder(self, df, exceptions=[]):

        for column in df:
            if column in exceptions:
                continue

            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype,
                                                                                               np.dtype(int).type):
                df = pd.get_dummies(df, columns=[column])
        return df

    def prepare_labels(self, data):

        if Globals.MULTI_LABEL:

            columns = data.columns.values
            label_columns = [column_name for column_name in columns if "label" in column_name]
            labels_to_rename = ['label_month_1', 'label_month_2', 'label_month_3', 'label_month_4', 'label_month_5',
                                'label_month_6', 'label_month_7', 'label_month_8', 'label_month_9', 'label_month_10',
                                'label_month_11', 'label_month_12', 'label_month_13', 'label_month_14',
                                'label_month_15',
                                'label_month_16', 'label_month_17', 'label_month_18']

            if set(labels_to_rename).issubset(set(label_columns)):
                data = data.rename(columns={'label_month_1': 'label_1_month', 'label_month_2': 'label_2_month',
                                            'label_month_3': 'label_3_month', 'label_month_4': 'label_4_month',
                                            'label_month_5': 'label_5_month', 'label_month_6': 'label_6_month',
                                            'label_month_7': 'label_7_month', 'label_month_8': 'label_8_month',
                                            'label_month_9': 'label_9_month', 'label_month_10': 'label_10_month',
                                            'label_month_11': 'label_11_month', 'label_month_12': 'label_12_month',
                                            'label_month_13': 'label_13_month', 'label_month_14': 'label_14_month',
                                            'label_month_15': 'label_15_month', 'label_month_16': 'label_16_month',
                                            'label_month_17': 'label_17_month', 'label_month_18': 'label_18_month'})
            columns = data.columns.values
            label_columns = [column_name for column_name in columns if "label" in column_name]

            # SELECT Labels
            labels = ['label_good_bad_loan', 'label_prepaid_ratio', 'label_month_final']

            for column in data.columns.values:
                if column in labels:
                    data = data.drop(column, 1)

            for label in labels:
                data[label] = data[label].astype(str)

        if Globals.GOOD_BAD_LABEL:

            columns = data.columns.values
            label_columns = [column_name for column_name in columns if "label" in column_name]

            columns = data.columns.values
            label_columns = [column_name for column_name in columns if "label" in column_name]

            # SELECT Labels
            labels = ['label_good_bad_loan']

            for column in data.columns.values:
                if column not in labels and column in label_columns:
                    data = data.drop(column, 1)

            for label in labels:
                data[label] = data[label].astype(str)

        if Globals.PREPAID_RATIO:

            columns = data.columns.values
            label_columns = [column_name for column_name in columns if "label" in column_name]

            # SELECT Labels
            labels = ['label_prepaid_ratio']

            for column in data.columns.values:
                if column not in labels and column in label_columns:
                    data = data.drop(column, 1)

        return data

    def combine_sums(self):

        # def get_data_i_raw(i):
        #     data_origin = DataParser().AmericanOrigination_i(i)
        #     data_monthly = DataParser().AmericanMonthly_i(i)
        #     df = FeatureExtraction().combine_data_and_origin(data_origin, data_monthly)
        #     return df
        #
        # def write_out_data(df_in, i):
        #     print "Writing out data"
        #     DataParser()._write_HDFStore_Combined(df_in, i)
        #
        # data_count = DataParser().number_of_datasets
        # # data_count = 1  # STOP FOR TESTING PURPOSES!!!!!
        # i = 0
        #
        # while i < data_count:
        #     print "Pre " + str(i) + " "
        #
        #     # WRITE OUT DATA TO FILE
        #     write_out_data(get_data_i_raw(i), i)
        #
        #     i = i + 1

        cols_to_sum_st = ['new_loans_per_state', 'occr_default_per_state', 'occr_paid_off_per_state',
                          'new_loans_per_state_12_mon', 'occr_paid_off_per_state_12_mon',
                          'occr_default_per_state_12_mon', 'active_loans_per_state']

        cols_to_sum_zip = ['new_loans_per_zipcode', 'occr_default_per_zipcode', 'occr_paid_off_per_zipcode',
                           'new_loans_per_zipcode_12_mon', 'occr_paid_off_per_zipcode_12_mon',
                           'occr_default_per_zipcode_12_mon', 'active_loans_per_zipcode']

        # self._combine_sums('st', cols_to_sum_st)
        self._combine_sums('zipcode', cols_to_sum_zip)


    def _combine_sums(self, ST_OR_ZIP, cols_to_sum):

        # def get_data_i_FE(i):
        #     return DataParser().AmericanCombo_i_FE(i)

        def get_data_i_FE2(i):
            return DataParser().AmericanCombo_i_FE2(i)

        def write_out_data(df, i):
            print "Writing out data"
            DataParser()._write_HDFStore_Combined_FE2(df, i)

        cols_sum = [col + '_sum' for col in cols_to_sum]

        df_store = pd.DataFrame(columns=['svcg_cycle', ST_OR_ZIP] + cols_sum)

        data_count = DataParser().number_of_datasets
        # data_count = 3  # STOP FOR TESTING PURPOSES!!!!!

        # i = 0
        #
        # while i < data_count:
        #
        #     print "A" + str(i) + " " + ST_OR_ZIP
        #
        #     # Get fetch current data
        #     df_active = get_data_i_FE2(i)
        #     df_active.reset_index(drop=True, inplace=True)
        #
        #     for COL_TO_SUM in cols_to_sum:
        #         COL_SUM = COL_TO_SUM + '_sum'
        #
        #         df_current = df_active[['svcg_cycle', ST_OR_ZIP, COL_TO_SUM]]
        #
        #         # Sum duplicates cuased by fragmentation
        #         df_current.loc[:, COL_TO_SUM] = df_current.groupby(['svcg_cycle', ST_OR_ZIP])[COL_TO_SUM].apply(
        #             lambda x: x.cumsum() + sum(np.unique(x)) - x.cumsum())
        #
        #         # Remove duplicate entries
        #         df_current = df_current.drop_duplicates(subset=['svcg_cycle', ST_OR_ZIP], keep='last')
        #         # Merge outer
        #         df_store = pd.merge(df_store, df_current, on=['svcg_cycle', ST_OR_ZIP], how='outer')
        #         # set nan to 0's
        #         df_store.loc[pd.isnull(df_store[COL_SUM]), COL_SUM] = 0
        #         df_store.loc[pd.isnull(df_store[COL_TO_SUM]), COL_TO_SUM] = 0
        #
        #         # Add number of occurences in current to overall total
        #         df_store.loc[:, COL_SUM] = df_store[COL_SUM] + df_store[COL_TO_SUM]
        #         # drop column
        #         df_store = df_store.drop(COL_TO_SUM, 1)
        #         # Sum duplicate entries
        #         df_store.loc[:, COL_SUM] = df_store.groupby(['svcg_cycle', ST_OR_ZIP])[COL_SUM].apply(
        #             lambda x: x.cumsum() + sum(x) - x.cumsum())
        #
        #         # Remove duplicate entries
        #         df_store = df_store.drop_duplicates(subset=['svcg_cycle', ST_OR_ZIP], keep='last')
        #     i += 1
        #
        # # Get cummax of occr columns
        # if ST_OR_ZIP == 'st':
        #     total_cols_st = ['new_loans_per_state', 'occr_default_per_state', 'occr_paid_off_per_state']
        #     df_store = df_store.sort_values(['st', 'svcg_cycle'], ascending=[True, True])
        #     for col in total_cols_st:
        #         col_sum = col + '_sum'
        #         if col_sum in df_store.columns.values:
        #             df_store[col_sum] = df_store.groupby(['st'])[col_sum].transform(lambda v: v.cummax())
        # else:
        #     total_cols_zip = ['new_loans_per_zipcode', 'occr_default_per_zipcode', 'occr_paid_off_per_zipcode']
        #     df_store = df_store.sort_values(['zipcode', 'svcg_cycle'], ascending=[True, True])
        #     for col in total_cols_zip:
        #         col_sum = col + '_sum'
        #         if col_sum in df_store.columns.values:
        #             df_store[col_sum] = df_store.groupby(['zipcode'])[col_sum].transform(lambda v: v.cummax())
        #
        # i = 0
        #
        # while i < data_count:
        #
        #     print "B" + str(i) + " " + ST_OR_ZIP
        #
        #     # Get fetch current data
        #     df_current = get_data_i_FE2(i)
        #
        #     for COL_TO_SUM in cols_to_sum:
        #         COL_SUM = COL_TO_SUM + '_sum'
        #         df_store_tmp = df_store[['svcg_cycle', ST_OR_ZIP, COL_SUM]]
        #         df_current = pd.merge(df_current, df_store_tmp, on=['svcg_cycle', ST_OR_ZIP], how='left')
        #         df_current.loc[:, COL_TO_SUM] = df_current[COL_SUM]
        #         df_current.loc[:, COL_TO_SUM] = df_current[COL_TO_SUM].astype(int)
        #         df_current = df_current.drop(COL_SUM, 1)
        #     # WRITE OUT DATA TO FILE
        #     write_out_data(df_current, i)
        #
        #     i += 1

        i = 26

        while i < data_count:

            print "C" + str(i) + " " + ST_OR_ZIP

            # Get fetch current data
            df_current = get_data_i_FE2(i)

            df_current['ones'] = 1
            df_current['small'] = 0.0001

            # default rate by zipcode
            df_current.loc[:, 'rt_default_per_zipcode'] = (df_current['occr_default_per_zipcode'] + df_current['small']) / (df_current['new_loans_per_zipcode'] + df_current['ones'])
            df_current.loc[:, 'rt_default_per_zipcode'] = df_current['rt_default_per_zipcode'].astype(float)

            # default rate by zipcode in last 12 months
            df_current.loc[:, 'rt_default_per_zipcode_12_mon'] = (df_current['occr_default_per_zipcode_12_mon'] +  df_current['small']) / (df_current['active_loans_per_zipcode'] + df_current['ones'])
            df_current.loc[:, 'rt_default_per_zipcode_12_mon'] = df_current['rt_default_per_zipcode_12_mon'].astype(float)

            #  ----------------------------------------

            # default rate by state
            df_current.loc[:, 'rt_default_per_state'] = (df_current['occr_default_per_state'] + df_current['small']) / (df_current['new_loans_per_state'] + df_current['ones'])
            df_current.loc[:, 'rt_default_per_state'] = df_current['rt_default_per_state'].astype(float)

            # default rate by state in last 12 months
            df_current.loc[:, 'rt_default_per_state_12_mon'] = (df_current['occr_default_per_state_12_mon'] + df_current['small']) / (df_current['active_loans_per_state'] + df_current['ones'])
            df_current.loc[:, 'rt_default_per_state_12_mon'] = df_current['rt_default_per_state_12_mon'].astype(float)

            cols_str = ['st', 'id_loan', 'flag_fthb', 'occpy_sts', 'channel', 'prod_type', 'prop_type', 'loan_purpose',
                        'repch_flag', 'flag_mod']
            for col_str in cols_str:
                df_current.loc[:, col_str] = df_current[col_str].astype(str)

            cols_int = ['ppmt_pnlty', 'delq_sts', 'net_sale_proceeds', 'occpy_sts']
            for col_int in cols_int:
                df_current.loc[:, col_int] = df_current[col_int].astype(str)

            # WRITE OUT DATA TO FILE
            write_out_data(df_current, i)

            i += 1

    def get_info_A(self):
        def get_data_i_FE2(i):
            print "Read" + str(i)
            return DataParser().AmericanCombo_i_FE2(i)

        def write_out_data(df, i):
            print "Writing out data"
            DataParser()._write_HDFStore_Combined_FE2(df, i)

        data_count = DataParser().number_of_datasets
        i = 0

        df_ALL = pd.DataFrame()
        df_ALL2 = pd.DataFrame()

        LOAN_COUNT = 0
        FICO_MEAN = 0
        FICO_MEDIAN = []
        BALANCE_MEAN = 0

        while i < data_count:

            df_X = get_data_i_FE2(i)

            df_X = df_X.sort_values("id_loan")
            df_X.reset_index(drop=True, inplace=True)
            n = 20000
            if len(df_X) < n:
                n = len(df_X)
            df_ALL = pd.concat([df_X[:n], df_ALL], axis=0)

            m = 5000
            if len(df_X) < m:
                m = len(df_X)
            df_ALL2 = pd.concat([df_X[:m], df_ALL2], axis=0)

            # LOAN_COUNT += len(np.unique(df_X['id_loan'].values))
            # FICO_MEAN += df_X['fico'].mean()
            # BALANCE_MEAN += df_X['orig_upb'].mean()
            # FICO_MEDIAN.append(df_X['fico'].median())
            # FICO_MEDIAN.append(df_X['fico'].median())
            i += 1

        FICO_MEAN = FICO_MEAN / i
        FICO_MEDIAN = np.median(FICO_MEDIAN)

        print "FICO_MEDIAN: " + str(FICO_MEDIAN)
        print "FICO_MEAN: " + str(FICO_MEAN)
        print "LOAN_COUNT: " + str(LOAN_COUNT)
        print "BALANCE_MEAN: " + str(BALANCE_MEAN)

        write_out_data(df_ALL, -1)
        write_out_data(df_ALL2, -2)


        # # Correct loan_age
        # df_current['ones'] = 1
        # df_current['loan_age'] = df_current.groupby(['id_loan'])['ones'].cumsum() - df_current['ones']
        # df_current = df_current.drop('ones', 1)


    def get_info_NLP(self):
        def get_data_i_FE2(i):
            print "Read" + str(i)
            return DataParser().AmericanCombo_i_FE2(i)

        def write_out_data(df, i):
            print "Writing out data"
            DataParser()._write_HDFStore_Combined_FE2(df, i)

        data_count = DataParser().number_of_datasets
        i = 0

        df_ALL = pd.DataFrame()
        df_ALL2 = pd.DataFrame()

        LOAN_COUNT = 0
        FICO_MEAN = 0
        FICO_MEDIAN = []
        BALANCE_MEAN = 0
        LOAN_LENGTH_MEAN = 0
        DEFAULT_LOANS_COUNT = 0
        FULLY_PAID_LOANS_COUNT = 0


        while i < data_count:

            df_IN = get_data_i_FE2(i)

            # Find all loans that have instance of 90-dd
            df = df_IN.loc[df_IN['status_month_0'] == 3]
            loan_ids_with_90_dd = df['id_loan'].unique()
            mask = df_IN['id_loan'].isin(loan_ids_with_90_dd)
            df_with_90_dd = df_IN.loc[mask]

            # Removes all updates that occured before loan FIRST became 90-dd, i.e. when loan becomes non-performing
            df_with_90_dd = df_with_90_dd.sort_values(['id_loan', 'svcg_cycle'], ascending=[True, True])
            df_with_90_dd['90_dd'] = 0
            df_with_90_dd.loc[df_with_90_dd['status_month_0'] == 3, '90_dd'] = 1
            df_with_90_dd['90_dd'] = df_with_90_dd.groupby(['id_loan'])['90_dd'].apply(lambda x: x.cumsum())
            df_with_90_dd = df_with_90_dd.loc[df_with_90_dd['90_dd'] != 0]
            df_with_90_dd = df_with_90_dd.drop('90_dd', 1)

            # print df_with_90_dd[['id_loan', 'svcg_cycle','st', 'status_month_0', 'occr_30dd', ]]

            df_np = df_with_90_dd

            LOAN_COUNT += len(np.unique(df_np['id_loan'].values))
            FICO_MEAN += df_np['fico'].mean()
            BALANCE_MEAN += df_np['orig_upb'].mean()
            FICO_MEDIAN.append(df_np['fico'].median())
            LOAN_LENGTH_MEAN += df_np.groupby(['id_loan']).size().mean()
            DEFAULT_LOANS_COUNT += len(df_np.loc[df_np['label_good_bad_loan'] == 0]['id_loan'].unique())
            FULLY_PAID_LOANS_COUNT += len(df_np.loc[df_np['label_good_bad_loan'] == 1]['id_loan'].unique())

            df_np = df_np.sort_values("id_loan")
            df_np.reset_index(drop=True, inplace=True)
            # n = 10000
            # if len(df_X) < n:
            #     n = len(df_X)
            # df_ALL = pd.concat([df_X[:n], df_ALL], axis=0)

            m = 20000
            if len(df_np) < m:
                m = len(df_np)
            df_ALL2 = pd.concat([df_np[:m], df_ALL2], axis=0)

            i += 1

        LOAN_COUNT = LOAN_COUNT
        FICO_MEAN = FICO_MEAN / i
        BALANCE_MEAN = BALANCE_MEAN / i
        LOAN_LENGTH_MEAN = LOAN_LENGTH_MEAN / i
        FICO_MEDIAN = np.median(FICO_MEDIAN)

        print "LOAN_LENGTH_MEAN: " + str(LOAN_LENGTH_MEAN)
        print "FICO_MEDIAN: " + str(FICO_MEDIAN)
        print "FICO_MEAN: " + str(FICO_MEAN)
        print "LOAN_COUNT: " + str(LOAN_COUNT)
        print "BALANCE_MEAN: " + str(BALANCE_MEAN)
        print "DEFAULT_LOANS_COUNT: " + str(DEFAULT_LOANS_COUNT)
        print "FULLY_PAID_LOANS_COUNT: " + str(FULLY_PAID_LOANS_COUNT)

        # write_out_data(df_ALL, -3)
        write_out_data(df_ALL2, -3)


        # # Correct loan_age
        # df_current['ones'] = 1
        # df_current['loan_age'] = df_current.groupby(['id_loan'])['ones'].cumsum() - df_current['ones']
        # df_current = df_current.drop('ones', 1)

    def get_info_BOTH(self):
        def get_data_i_FE2(i):
            print "Read" + str(i)
            return DataParser().AmericanCombo_i_FE2(i)

        def write_out_data(df, i):
            print "Writing out data"
            DataParser()._write_HDFStore_Combined_FE2(df, i)

        data_count = DataParser().number_of_datasets
        i = 0

        df_ALL = pd.DataFrame()
        df_ALL2 = pd.DataFrame()

        LOAN_COUNT = 0
        FICO_MEAN = 0
        FICO_MEDIAN = []
        BALANCE_MEAN = 0

        while i < data_count:

            df_X = get_data_i_FE2(i)
            df_IN = df_X.copy()


            df_X = df_X.sort_values("id_loan")
            df_X.reset_index(drop=True, inplace=True)
            n = 20000
            if len(df_X) < n:
                n = len(df_X)
            df_ALL = pd.concat([df_X[:n], df_ALL], axis=0)





            # Find all loans that have instance of 90-dd
            df = df_IN.loc[df_IN['status_month_0'] == 3]
            loan_ids_with_90_dd = df['id_loan'].unique()
            mask = df_IN['id_loan'].isin(loan_ids_with_90_dd)
            df_with_90_dd = df_IN.loc[mask]

            # Removes all updates that occured before loan FIRST became 90-dd, i.e. when loan becomes non-performing
            df_with_90_dd = df_with_90_dd.sort_values(['id_loan', 'svcg_cycle'], ascending=[True, True])
            df_with_90_dd['90_dd'] = 0
            df_with_90_dd.loc[df_with_90_dd['status_month_0'] == 3, '90_dd'] = 1
            df_with_90_dd['90_dd'] = df_with_90_dd.groupby(['id_loan'])['90_dd'].apply(lambda x: x.cumsum())
            df_with_90_dd = df_with_90_dd.loc[df_with_90_dd['90_dd'] != 0]
            df_with_90_dd = df_with_90_dd.drop('90_dd', 1)

            # print df_with_90_dd[['id_loan', 'svcg_cycle','st', 'status_month_0', 'occr_30dd', ]]

            df_np = df_with_90_dd

            df_np = df_np.sort_values("id_loan")
            df_np.reset_index(drop=True, inplace=True)
            # n = 10000
            # if len(df_X) < n:
            #     n = len(df_X)
            # df_ALL = pd.concat([df_X[:n], df_ALL], axis=0)

            # m = 20000
            # if len(df_np) < m:
            #     m = len(df_np)
            df_ALL2 = pd.concat([df_np, df_ALL2], axis=0)


            i += 1



        write_out_data(df_ALL, -1)
        write_out_data(df_ALL2, -3)


        # # Correct loan_age
        # df_current['ones'] = 1
        # df_current['loan_age'] = df_current.groupby(['id_loan'])['ones'].cumsum() - df_current['ones']
        # df_current = df_current.drop('ones', 1)


if __name__ == "__main__":
    print "jkekr"