import pandas as pd
import numpy as np
import time


class FeatureExtraction:
    """ A class that parses input data from file. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """


    def filter_main(self, data):
        start_time = time.time()

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

        columns_allowed = columns + labels

        for column in data.columns.values:
            if column not in columns_allowed:
                data = data.drop(column, 1)
                # print "Removed column: " + column

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

        # Create row for each monthly update and concat with origin data
        data_ohc_all = pd.merge(data_template_ohc, data_ohc, how='right')

        # Make extra ohc vars = 0
        for column in data_template_ohc:
            data_ohc_all.loc[pd.isnull(data_ohc_all[column]), column] = 0

        if "label_good_bad_loan_0" not in data_ohc_all.columns:
            data_ohc_all.loc[:, 'label_good_bad_loan_0'] = '0'

        if "label_good_bad_loan_1" not in data_ohc_all.columns:
            data_ohc_all.loc[:, 'label_good_bad_loan_1'] = '0'

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

        columns = data.columns.values
        label_columns = [column_name for column_name in columns if "label" in column_name]

        # SELECT Labels
        labels = ['label_good_bad_loan']

        for column in data.columns.values:
            if column not in labels and column in label_columns:
                data = data.drop(column, 1)

        for label in labels:
            data[label] = data[label].astype(str)

        return data