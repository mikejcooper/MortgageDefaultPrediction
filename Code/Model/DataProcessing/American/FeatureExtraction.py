import pandas as pd
import numpy as np
import gc
import resource

from DataParser import DataParser



class FeatureExtraction:
    """ A class that parses input data from file. """

    INSPECT_LOANS_WITHOUT_FINAL_STATE = False
    PRINT_LOAN_BREAKDOWN = False
    TESTING = False

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        # self._dataFrame = data_frame
        # assert isinstance(self._dataFrame, pd.DataFrame)
        # print self._dataFrame.dtypes

        # self.ml_model(data_frame)

    def apply_all(self, df):
        assert isinstance(df, pd.DataFrame)

        # df = self.map_english_column_names(df)
        # df = self.one_hot_encoder(df, exceptions=['Predict'])
        print df.dtypes

        return df

    def combine_data_and_origin(self, data_origin, data_monthly):

        # return DataParser()._read_HDFStore_Combined(20)

        pd.options.mode.chained_assignment = None
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.width', 3000)

        # Add new loans to active
        active_loans = pd.DataFrame()
        active_loans = pd.concat([active_loans, data_origin], axis=0).drop_duplicates()

        # Isolate for testing
        if self.TESTING:
            active_loans = active_loans.head(100)
            data_monthly = data_monthly.head(10000)

        # Create row for each monthly update and concat with origin data
        active_loans_monthly = pd.merge(active_loans, data_monthly, on='id_loan', how='right')

        print "FICO NULL: " + str(active_loans_monthly['fico'].isnull().sum())

        # return active_loans_monthly

        # ---- FICO -----
        # Force to numerical or set to NAN
        active_loans_monthly['fico'] = pd.to_numeric(active_loans_monthly['fico'], errors='coerce')
        # Remove all rows where FICO has no value
        active_loans_monthly = active_loans_monthly.loc[pd.notnull(active_loans_monthly['fico'])]

        # Add label column
        active_loans_with_labels = active_loans_monthly
        active_loans_with_labels['delq_sts'] = active_loans_with_labels['delq_sts'].astype(str)
        active_loans_with_labels.loc[:, 'status_month_0'] = active_loans_with_labels['delq_sts']

        # ------------------------------ Label RULES -----------------------------



        # 3 : 90 + days delinquent,
        where_not_equal_to = active_loans_with_labels.query(
            "status_month_0 != '0' & status_month_0 != '1' & status_month_0 != '2'").index
        active_loans_with_labels.loc[where_not_equal_to, 'status_month_0'] = 3

        # -------------------- FINAL STATES -------------------------

        # 4 : Foreclosed (default),
        active_loans_with_labels.loc[active_loans_with_labels['cd_zero_bal'] == 3.0, 'status_month_0'] = 4
        active_loans_with_labels.loc[active_loans_with_labels['cd_zero_bal'] == 6.0, 'status_month_0'] = 4

        # 5 : REO,
        active_loans_with_labels.loc[active_loans_with_labels['cd_zero_bal'] == 9.0, 'status_month_0'] = 5
        active_loans_with_labels.loc[active_loans_with_labels['status_month_0'] == 'R', 'status_month_0'] = 5

        # 6 : paid off
        active_loans_with_labels.loc[active_loans_with_labels['cd_zero_bal'] == 1.0, 'status_month_0'] = 6
        active_loans_with_labels.loc[active_loans_with_labels['repch_flag'] == 'N', 'status_month_0'] = 6

        # ------------------ FINAL STATES -------------------------

        # 0 : Current, # 1 : 30 days delinquent, # 2 : 60 days delinquent,
        active_loans_with_labels.loc[:, 'status_month_0'] = active_loans_with_labels['status_month_0'].astype(int)

        # ------------------------------ Label RULES -----------------------------

        if self.INSPECT_LOANS_WITHOUT_FINAL_STATE:
            self.inspect_loans_without_final_state(active_loans_with_labels)

        # Only use loans that have final state
        where_equal_to_final_state = active_loans_with_labels.query(
            "status_month_0 == 6 | status_month_0 == 5 | status_month_0 == 4").index
        useable_loan_ids = active_loans_with_labels.loc[where_equal_to_final_state]['id_loan']
        loans_with_final_state = active_loans_with_labels.loc[
            active_loans_with_labels['id_loan'].isin(useable_loan_ids)]



        # ---------------------- Split Data -------------------------------------
        #
        # # Fragment large dataframe
        # import math
        # df1 = loans_with_final_state
        # df1 = df1.sort_values("id_loan", ascending=True)
        # df1.reset_index(inplace=True)
        # ids = df1['id_loan'].unique()
        # length = len(ids)
        # split = 1
        # fragment = int(math.floor(length / split))
        #
        # df_frag = pd.DataFrame()
        # for i in range(0, split):
        #     import time
        #     start = time.time()
        #     print i
        #
        #     start_index = df1.loc[df1['id_loan'] == ids[i * fragment]].index.values[0]
        #     end_index = df1.loc[df1['id_loan'] == ids[(i + 1) * fragment - 1]].index.values[-1]
        #
        #     df_frag_i = df1.iloc[start_index:end_index]
        #
        #
        #     print "length = " + str(len(df_frag_i))
        #
        #
        #     # ------------ Perform operation -------------
        #
        #     label_columns, df_frag_i = self.create_labels(df_frag_i)
        #
        #     # -----------------------------------------------------------------------------------------
        #     # Select information from loan origination date only, remove monthly updates.
        #     # df1 = loans_with_final_state.sort_values("svcg_cycle", ascending=True)
        #     # df_unique_loan_id = df1['id_loan'].drop_duplicates().index
        #     # start_loans = df1.loc[df_unique_loan_id]
        #     # loans_with_final_state = start_loans
        #     # -----------------------------------------------------------------------------------------
        #
        #     df_frag_i = self.filter_data(df_frag_i)
        #
        #     if len(df_frag_i) == 0:
        #         continue
        #
        #     # ------------ Perform operation -------------
        #
        #     # Concat back together
        #     if len(df_frag) < 5:
        #         df_frag = df_frag_i
        #     else:
        #         df_frag = df_frag.append(df_frag_i)
        #
        #     end = time.time()
        #     print("time: " +str(end - start))
        #
        # df = df_frag

        # ---------------------- Split Data -------------------------------------
        import time
        print "TIME START ..."
        start = time.time()

        print "   length = " + str(len(loans_with_final_state))
        df = loans_with_final_state
        label_columns, df = self.create_labels(df)

        # -----------------------------------------------------------------------------------------
        # Select information from loan origination date only, remove monthly updates.
        # df1 = loans_with_final_state.sort_values("svcg_cycle", ascending=True)
        # df_unique_loan_id = df1['id_loan'].drop_duplicates().index
        # start_loans = df1.loc[df_unique_loan_id]
        # loans_with_final_state = start_loans
        # -----------------------------------------------------------------------------------------

        df = self.filter_data(df)

        df = self.filter_data_monthly(df)

        df = self.filter_local_factors(df)

        end = time.time()
        print("time: " + str(end - start))



        return df



    def create_labels(self, loans_with_final_state):

        # Sort into order
        loans_with_final_state = loans_with_final_state.sort_values(['id_loan', 'svcg_cycle'], ascending=[True, True])

        # Creates labels for monthly period look ahead
        months_to_track = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        status_columns = ['status_month_0']
        where_equal_to_final_state_label = loans_with_final_state.query(
            "status_month_0 == 6 | status_month_0 == 5 | status_month_0 == 4").index
        for i in range(1, max(months_to_track) + 1):
            status_columns.append("label_month_" + str(i))
            loans_with_final_state.loc[:, status_columns[i]] = loans_with_final_state[status_columns[i - 1]].shift(-1)
            loans_with_final_state.loc[where_equal_to_final_state_label, status_columns[i]] = loans_with_final_state.loc[where_equal_to_final_state_label, status_columns[i - 1]]

        for i in range(0, max(months_to_track) + 1):
            if i not in months_to_track:
                loans_with_final_state = loans_with_final_state.drop(status_columns[i], 1)
            else:
                loans_with_final_state.loc[pd.isnull(loans_with_final_state[status_columns[i]]), status_columns[i]] = 0
                loans_with_final_state[status_columns[i]] = loans_with_final_state[status_columns[i]].astype('int64')

        # Create label_month_final LABEL
        df = loans_with_final_state.sort_values("svcg_cycle", ascending=False)
        index_last_loan_entries = df['id_loan'].drop_duplicates().index
        df_last_loan_entries = df.loc[index_last_loan_entries]
        df_last_loan_entries = df_last_loan_entries[['status_month_0', 'id_loan']]
        df_last_loan_entries = df_last_loan_entries.rename(columns={'status_month_0': 'label_month_final'})
        df_with_final_label = pd.merge(df_last_loan_entries, df, on='id_loan', how='right')
        df = df_with_final_label

        # Create label_good_bad_loan LABEL
        df = df.sort_values("svcg_cycle", ascending=False)
        index_last_loan_entries = df['id_loan'].drop_duplicates().index
        df_last_loan_entries = df.loc[index_last_loan_entries]
        df_last_loan_entries = df_last_loan_entries[['label_month_final', 'id_loan']]
        df_last_loan_entries.loc[df_last_loan_entries['label_month_final'] == 6, 'label_month_final'] = 1
        df_last_loan_entries.loc[df_last_loan_entries['label_month_final'] != 1, 'label_month_final'] = 0
        df_last_loan_entries = df_last_loan_entries.rename(columns={'label_month_final': 'label_good_bad_loan'})
        df_with_final_label = pd.merge(df_last_loan_entries, df, on='id_loan', how='right')
        df = df_with_final_label



        columns = df.columns.values
        label_columns = [column_name for column_name in columns if "label" in column_name]
        return (label_columns, df)



    def filter_data(self, data):

        # Only accept row within range
        data['fico'] = data['fico'].astype(float)
        data = data.loc[data['fico'] < 1000]
        data = data.loc[data['fico'] > 0]

        # ---- dt_first_pi ----
        # Only allow data with date of initial payment ** maybe change this
        data = data.loc[pd.notnull(data['dt_first_pi'])]
        data['dt_first_pi'] = data['dt_first_pi'].astype(float)

        # ---- flag_fthb - FIRST TIME HOMEBUYER FLAG ------   * could so something clever here
        data.loc[~data['flag_fthb'].isin(['Y', 'N']), 'flag_fthb'] = 'U'

        # ----- cnt_units ----------
        data['cnt_units'] = pd.to_numeric(data['cnt_units'], errors='coerce')
        data.loc[~data['cnt_units'].isin([1, 2, 3, 4]), 'cnt_units'] = data.loc[data['cnt_units'].isin([1, 2, 3, 4])][
            'cnt_units'].median()
        data['cnt_units'] = data['cnt_units'].astype(float)

        # ----- occpy_sts ----------
        data.loc[~data['occpy_sts'].isin(['O', 'I', 'S']), 'occpy_sts'] = 'U'

        # ----- channel ----------
        data.loc[~data['channel'].isin(['R', 'B', 'C', 'T']), 'channel'] = 'U'

        # ----- ppmt_pnlty ----------
        data.loc[~data['ppmt_pnlty'].isin(['Y', 'N']), 'ppmt_pnlty'] = 'U'

        # ----- prod_type ----------
        data.loc[~data['prod_type'].isin(['FRM']), 'prod_type'] = 'U'

        # ----- prop_type ----------
        data.loc[~data['prop_type'].isin(['SF', 'PU', 'CO', 'MH', 'CP', 'LH']), 'prop_type'] = 'U'

        # ----- loan_purpose ----------
        data.loc[~data['loan_purpose'].isin(['L', 'N', 'C']), 'loan_purpose'] = 'U'

        # ----- current_upb ----------
        # Only allow data with current mortgage balance
        data = data.loc[pd.notnull(data['current_upb'])]
        data['current_upb'] = data['current_upb'].astype(float)

        convert_features = ['current_int_rt', 'loan_age', 'svcg_cycle', 'cnt_borr', 'orig_loan_term', 'zipcode',
                            'cd_msa', 'mi_pct', 'cltv', 'dti', 'orig_upb', 'int_rt', 'ltv',
                            'cd_zero_bal']

        data = self.convert_to_num_fill_with_median(data, convert_features)

        # ----- servicer_name ---------- Not sure what to do with this
        data = data.drop('servicer_name', 1)
        #
        # # ----- seller_name ---------- Not sure what to do with this
        data = data.drop('seller_name', 1)


        to_type_str = ['st', 'id_loan', 'flag_fthb', 'occpy_sts', 'channel', 'ppmt_pnlty', 'prod_type', 'prop_type', 'loan_purpose', 'delq_sts', 'repch_flag', 'flag_mod', 'net_sale_proceeds']

        for column in to_type_str:
            data[column] = data[column].astype(str)

        # return data



        # Values in sample are nan


        return data

    def convert_to_num_fill_with_median(self, data, features):
        for feature in features:
            # Force to numerical or set to NAN
            data[feature] = pd.to_numeric(data[feature], errors='coerce')
            # Set nan values to median of non NAN values
            data.loc[pd.isnull(data[feature]), feature] = data.loc[pd.notnull(data[feature])][feature].median()
            data[feature] = data[feature].astype(float)
        return data

    def filter_data_monthly(self, data):
        columns__monthly = ['delq_sts', 'svcg_cycle', 'current_upb', 'loan_age', 'mths_remng', 'current_int_rt']

        df_main = data

        # Introduce new dataset - national housing price index per state
        df_hous_prc_indx = DataParser().national_housing_price_index()
        df_main = pd.merge(df_hous_prc_indx, df_main, left_on=['svcg_cycle', 'st'], right_on=['svcg_cycle', 'st'],
                           how='right')

        # Introduce new dataset - national unemployment rates per state
        df_unemploy_rt = DataParser().national_unemploy_rt()
        df_main = pd.merge(df_unemploy_rt, df_main, left_on=['svcg_cycle', 'st'], right_on=['svcg_cycle', 'st'],
                           how='right')

        # Introduce new dataset - national mortgage rate
        df_nat_int_rt = DataParser().national_mortgage_rate()
        df_main = pd.merge(df_nat_int_rt, df_main, on='svcg_cycle', how='right')

        # Initialise new columns
        df_main.loc[:, 'time_since_origin'] = 1

        df_main.loc[:, 'pct_change'] = 0
        df_main.loc[:, 'crt_minus_nat_int_rt'] = 0
        df_main.loc[:, 'occr_crt_less_than_nat_int_rate'] = 0
        df_main.loc[:, 'label_prepaid_ratio'] = 0

        df_main.loc[:, 'occr_curr_12_mon'] = 0
        df_main.loc[:, 'occr_curr'] = 0

        df_main.loc[:, 'occr_30dd_12_mon'] = 0
        df_main.loc[:, 'occr_30dd'] = 0

        df_main.loc[:, 'occr_60dd_12_mon'] = 0
        df_main.loc[:, 'occr_60dd'] = 0

        df_main.loc[:, 'occr_90dd_12_mon'] = 0
        df_main.loc[:, 'occr_90dd'] = 0

        df_main.loc[:, 'occr_foreclosed_12_mon'] = 0
        df_main.loc[:, 'occr_foreclosed'] = 0

        # Fill new columns

        # ORDER DATA
        df_main = df_main.sort_values(['id_loan', 'svcg_cycle'], ascending=[True, True])

        # Time since origin
        df_main['time_since_origin'] = df_main.groupby(['id_loan'])['time_since_origin'].apply(lambda x: x.cumsum())

        # ----------------------------------------------------------------------

        # Current interest rate - national mortage rate
        df_main['crt_minus_nat_int_rt'] = df_main['current_int_rt'] - df_main['nat_int_rt']

        # ----------------------------------------------------------------------

        # Number of occurrences of current
        query = df_main.query("status_month_0 == 0").index
        df_main.loc[query, 'occr_curr'] = 1
        df_main['occr_curr'] = df_main.groupby(['id_loan'])['occr_curr'].apply(lambda x: x.cumsum())

        # Number of occurrences of current in last 12 months
        df_main.loc[:, 'occr_curr_12_mon'] = df_main['occr_curr'] - df_main.groupby(['id_loan'])['occr_curr'].shift(12)
        df_main['occr_curr_12_mon'] = df_main['occr_curr_12_mon'].fillna(df_main['occr_curr'])

        # ----------------------------------------------------------------------

        # Number of occurrences of 30 days delinquent
        query = df_main.query("status_month_0 == 1").index
        df_main.loc[query, 'occr_30dd'] = 1
        df_main['occr_30dd'] = df_main.groupby(['id_loan'])['occr_30dd'].apply(lambda x: x.cumsum())

        # Number of occurrences of 30 days delinquent in last 12 months
        df_main.loc[:, 'occr_30dd_12_mon'] = df_main['occr_30dd'] - df_main.groupby(['id_loan'])['occr_30dd'].shift(12)
        df_main['occr_30dd_12_mon'] = df_main['occr_30dd_12_mon'].fillna(df_main['occr_30dd'])

        # ----------------------------------------------------------------------

        # Number of occurrences of 60 days delinquent
        query = df_main.query("status_month_0 == 2").index
        df_main.loc[query, 'occr_60dd'] = 1
        df_main['occr_60dd'] = df_main.groupby(['id_loan'])['occr_60dd'].apply(lambda x: x.cumsum())

        # Number of occurrences of 60 days delinquent in last 12 months
        df_main.loc[:, 'occr_60dd_12_mon'] = df_main['occr_60dd'] - df_main.groupby(['id_loan'])['occr_60dd'].shift(12)
        df_main['occr_60dd_12_mon'] = df_main['occr_60dd_12_mon'].fillna(df_main['occr_60dd'])

        # ----------------------------------------------------------------------

        # Number of occurrences of 90+ days delinquent
        query = df_main.query("status_month_0 > 2").index
        df_main.loc[query, 'occr_90dd'] = 1
        df_main['occr_90dd'] = df_main.groupby(['id_loan'])['occr_90dd'].apply(lambda x: x.cumsum())

        # Number of occurrences of 90+ days delinquent in last 12 months
        df_main.loc[:, 'occr_90dd_12_mon'] = df_main['occr_90dd'] - df_main.groupby(['id_loan'])['occr_90dd'].shift(12)
        df_main['occr_90dd_12_mon'] = df_main['occr_90dd_12_mon'].fillna(df_main['occr_90dd'])

        # ----------------------------------------------------------------------

        # Number of occurrences of Foreclosed
        query = df_main.query("status_month_0 == 4").index
        df_main.loc[query, 'occr_foreclosed'] = 1
        df_main['occr_foreclosed'] = df_main.groupby(['id_loan'])['occr_foreclosed'].apply(lambda x: x.cumsum())

        # Number of occurrences of Foreclosed in last 12 months
        df_main.loc[:, 'occr_foreclosed_12_mon'] = df_main['occr_foreclosed'] - df_main.groupby(['id_loan'])[
            'occr_foreclosed'].shift(12)
        df_main['occr_foreclosed_12_mon'] = df_main['occr_foreclosed_12_mon'].fillna(df_main['occr_foreclosed'])

        # ----------------------------------------------------------------------

        # Percentage change between last balance and current balance
        next_day_pct_change = df_main.groupby(['id_loan'])['current_upb'].shift(1)
        df_main['pct_change'] = (df_main['current_upb'] - next_day_pct_change) / next_day_pct_change
        df_main.loc[df_main['pct_change'] == -1.0, 'pct_change'] = 0
        df_main = df_main.fillna(0)

        # ----------------------------------------------------------------------

        # Number of months the mortgage's interest has been less than the national mortgage rate
        query = df_main.query("crt_minus_nat_int_rt < 0").index
        df_main.loc[query, 'occr_crt_less_than_nat_int_rate'] = 1
        df_main['occr_crt_less_than_nat_int_rate'] = df_main.groupby(['id_loan'])[
            'occr_crt_less_than_nat_int_rate'].apply(lambda x: x.cumsum())

        # ----------------------------------------------------------------------

        # Create pre-paid to original loan amount ratio label
        df_main['label_prepaid_ratio'] = df_main.groupby(['id_loan'])['orig_upb'].apply(lambda x: x / len(x))

        return df_main

    def filter_local_factors(self, df1):

        # ------------------ LOCAL FACTORS ------------------------
        df1.loc[:, 'ones'] = 1

        # Add 1 to first row of each loan id for cumsum operations
        df1.loc[:, 'one_per_loan'] = 0
        df1.loc[df1.groupby('id_loan', as_index=False).head(1).index, 'one_per_loan'] = 1

        # default loans
        df1.loc[:, 'default'] = 0
        df1.loc[df1['status_month_0'] == 4, 'default'] = 1
        df1.loc[df1['status_month_0'] == 5, 'default'] = 1

        # paid-off loans
        df1.loc[:, 'paid_off'] = 0
        df1.loc[df1['status_month_0'] == 6, 'paid_off'] = 1


        # ------------ Zipcode ----------------

        df1 = df1.sort_values(['zipcode', 'svcg_cycle'], ascending=[True, True])

        # Number of loans in local area by zipcode at time t (that have started)
        df_tmp = df1[['svcg_cycle', 'zipcode', 'id_loan']].drop_duplicates(subset='id_loan')
        df_tmp['ones'] = 1
        df_tmp['new_loans_per_zipcode'] = df_tmp.groupby(['svcg_cycle', 'zipcode'])['ones'].cumsum()
        df_tmp = df_tmp.drop_duplicates(subset=['svcg_cycle', 'zipcode'], keep='last')
        df_tmp['new_loans_per_zipcode'] = df_tmp.groupby(['zipcode'])['new_loans_per_zipcode'].cumsum()
        df_tmp = df_tmp.drop('id_loan', 1)
        df_tmp = df_tmp.drop('ones', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')
        df1 = df1.sort_values(['zipcode', 'svcg_cycle'], ascending=[False, False])
        df1['new_loans_per_zipcode'] = df1.groupby(['zipcode'])['new_loans_per_zipcode'].transform(lambda v: v.ffill())
        df1 = df1.sort_values(['zipcode', 'svcg_cycle'], ascending=[True, True])
        df1['new_loans_per_zipcode'] = df1.groupby(['zipcode'])['new_loans_per_zipcode'].transform(lambda v: v.ffill())

        # # Number of loans in local area by zipcode at time t (that have started finised)
        # df_tmp = df1[['svcg_cycle', 'zipcode', 'id_loan', 'status_month_0']].drop_duplicates(subset='id_loan', keep='last')
        # df_tmp['ones'] = 1
        # df_tmp = df_tmp.loc[df_tmp['status_month_0'] > 3]
        # df_tmp['completed_loans_per_zipcode'] = df_tmp.groupby(['svcg_cycle', 'zipcode'])['ones'].cumsum()
        # df_tmp = df_tmp.drop_duplicates(subset=['svcg_cycle', 'zipcode'], keep='last')
        # df_tmp['completed_loans_per_zipcode'] = df_tmp.groupby(['zipcode'])['completed_loans_per_zipcode'].cumsum()
        # df_tmp = df_tmp.drop('id_loan', 1)
        # df_tmp = df_tmp.drop('ones', 1)
        # df_tmp = df_tmp.drop('status_month_0', 1)
        # df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')
        # df1['completed_loans_per_zipcode'] = df1['completed_loans_per_zipcode'].fillna(0)

        # Number of ACTIVE loans in local area by zipcode at time t
        df_tmp = df1[['svcg_cycle', 'zipcode', 'id_loan']]
        df_tmp['ones'] = 1
        df_tmp['active_loans_per_zipcode'] = df_tmp.groupby(['svcg_cycle', 'zipcode'])['ones'].cumsum()
        df_tmp = df_tmp.drop_duplicates(subset=['svcg_cycle', 'zipcode'], keep='last')
        df_tmp = df_tmp.drop('id_loan', 1)
        df_tmp = df_tmp.drop('ones', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')
        df1['active_loans_per_zipcode'] = df1['active_loans_per_zipcode'].fillna(1)

        # Number of loans in local area by zipcode in last 12 months
        df_tmp = df1[['svcg_cycle', 'zipcode', 'new_loans_per_zipcode']].drop_duplicates(subset=['svcg_cycle', 'zipcode'])
        df_tmp.loc[:, 'new_loans_per_zipcode_12_mon'] = df_tmp['new_loans_per_zipcode'] - df_tmp.groupby(['zipcode'])[
            'new_loans_per_zipcode'].shift(12)
        df_tmp['new_loans_per_zipcode_12_mon'] = df_tmp['new_loans_per_zipcode_12_mon'].fillna(
            df_tmp['new_loans_per_zipcode'])
        df_tmp = df_tmp.drop('new_loans_per_zipcode', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')
        gc.collect()
        df1 = df1.sort_values(['zipcode', 'svcg_cycle'], ascending=[False, False])
        df1['new_loans_per_zipcode_12_mon'] = df1.groupby(['zipcode'])['new_loans_per_zipcode_12_mon'].transform(lambda v: v.ffill())
        df1 = df1.sort_values(['zipcode', 'svcg_cycle'], ascending=[True, True])
        df1['new_loans_per_zipcode_12_mon'] = df1.groupby(['zipcode'])['new_loans_per_zipcode_12_mon'].transform(lambda v: v.ffill())

        # paid_off loans by zipcode total and last 12 months
        df1['occr_paid_off_per_zipcode'] = df1.groupby(['svcg_cycle', 'zipcode'])['paid_off'].apply(
            lambda x: x.cumsum() + sum(x) - x.cumsum())
        df_tmp = df1[['svcg_cycle', 'zipcode', 'occr_paid_off_per_zipcode']].drop_duplicates()
        df_tmp['occr_paid_off_per_zipcode'] = df_tmp.groupby(['zipcode'])['occr_paid_off_per_zipcode'].cumsum()
        df_tmp['occr_paid_off_per_zipcode_12_mon'] = df_tmp['occr_paid_off_per_zipcode'] - df_tmp.groupby(['zipcode'])[
            'occr_paid_off_per_zipcode'].shift(12)
        df_tmp['occr_paid_off_per_zipcode_12_mon'] = df_tmp['occr_paid_off_per_zipcode_12_mon'].fillna(
            df_tmp['occr_paid_off_per_zipcode'])
        df1 = df1.drop('occr_paid_off_per_zipcode', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')

        # default loans by zipcode total and last 12 months
        df1['occr_default_per_zipcode'] = df1.groupby(['svcg_cycle', 'zipcode'])['default'].apply(
            lambda x: x.cumsum() + sum(x) - x.cumsum())
        df_tmp = df1[['svcg_cycle', 'zipcode', 'occr_default_per_zipcode']].drop_duplicates()
        df_tmp['occr_default_per_zipcode'] = df_tmp.groupby(['zipcode'])['occr_default_per_zipcode'].cumsum()
        df_tmp['occr_default_per_zipcode_12_mon'] = df_tmp['occr_default_per_zipcode'] - df_tmp.groupby(['zipcode'])[
            'occr_default_per_zipcode'].shift(12)
        df_tmp['occr_default_per_zipcode_12_mon'] = df_tmp['occr_default_per_zipcode_12_mon'].fillna(
            df_tmp['occr_default_per_zipcode'])
        df1 = df1.drop('occr_default_per_zipcode', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'zipcode'], how='right')

        # ------------ STATE ------------------

        df1 = df1.sort_values(['st', 'svcg_cycle'], ascending=[True, True])


        # Number of loans in local area by State at time t
        df_tmp = df1[['svcg_cycle', 'st', 'id_loan']].drop_duplicates(subset='id_loan')
        df_tmp['ones'] = 1
        df_tmp['new_loans_per_state'] = df_tmp.groupby(['svcg_cycle', 'st'])['ones'].cumsum()
        df_tmp = df_tmp.drop_duplicates(subset=['svcg_cycle', 'st'], keep='last')
        df_tmp['new_loans_per_state'] = df_tmp.groupby(['st'])['new_loans_per_state'].cumsum()
        df_tmp = df_tmp.drop('id_loan', 1)
        df_tmp = df_tmp.drop('ones', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'st'], how='right')
        df1 = df1.sort_values(['st', 'svcg_cycle'], ascending=[False, False])
        df1['new_loans_per_state'] = df1.groupby(['st'])['new_loans_per_state'].transform(lambda v: v.ffill())
        df1 = df1.sort_values(['st', 'svcg_cycle'], ascending=[True, True])
        df1['new_loans_per_state'] = df1.groupby(['st'])['new_loans_per_state'].transform(lambda v: v.ffill())

        # Number of ACTIVE loans in local area by st at time t
        df_tmp = df1[['svcg_cycle', 'st', 'id_loan']]
        df_tmp['ones'] = 1
        df_tmp['active_loans_per_state'] = df_tmp.groupby(['svcg_cycle', 'st'])['ones'].cumsum()
        df_tmp = df_tmp.drop_duplicates(subset=['svcg_cycle', 'st'], keep='last')
        df_tmp = df_tmp.drop('id_loan', 1)
        df_tmp = df_tmp.drop('ones', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'st'], how='right')
        df1['active_loans_per_state'] = df1['active_loans_per_state'].fillna(1)

        # Number of loans in local area by State in last 12 months
        df_tmp = df1[['svcg_cycle', 'st', 'new_loans_per_state']].drop_duplicates(subset=['svcg_cycle', 'st'])
        df_tmp.loc[:, 'new_loans_per_state_12_mon'] = df_tmp['new_loans_per_state'] - df_tmp.groupby(['st'])[
            'new_loans_per_state'].shift(12)
        df_tmp['new_loans_per_state_12_mon'] = df_tmp['new_loans_per_state_12_mon'].fillna(
            df_tmp['new_loans_per_state'])
        df_tmp = df_tmp.drop('new_loans_per_state', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'st'], how='right')
        df1 = df1.sort_values(['st', 'svcg_cycle'], ascending=[False, False])
        df1['new_loans_per_state_12_mon'] = df1.groupby(['st'])['new_loans_per_state_12_mon'].transform(lambda v: v.ffill())
        df1 = df1.sort_values(['st', 'svcg_cycle'], ascending=[True, True])
        df1['new_loans_per_state_12_mon'] = df1.groupby(['st'])['new_loans_per_state_12_mon'].transform(lambda v: v.ffill())

        # paid_off loans by state total and last 12 months
        df1['occr_paid_off_per_state'] = df1.groupby(['svcg_cycle', 'st'])['paid_off'].apply(
            lambda x: x.cumsum() + sum(x) - x.cumsum())
        df_tmp = df1[['svcg_cycle', 'st', 'occr_paid_off_per_state']].drop_duplicates()
        df_tmp['occr_paid_off_per_state'] = df_tmp.groupby(['st'])['occr_paid_off_per_state'].cumsum()
        df_tmp['occr_paid_off_per_state_12_mon'] = df_tmp['occr_paid_off_per_state'] - df_tmp.groupby(['st'])[
            'occr_paid_off_per_state'].shift(12)
        df_tmp['occr_paid_off_per_state_12_mon'] = df_tmp['occr_paid_off_per_state_12_mon'].fillna(
            df_tmp['occr_paid_off_per_state'])
        df1 = df1.drop('occr_paid_off_per_state', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'st'], how='right')

        # default loans by state total and last 12 months
        df1['occr_default_per_state'] = df1.groupby(['svcg_cycle', 'st'])['default'].apply(
            lambda x: x.cumsum() + sum(x) - x.cumsum())
        df_tmp = df1[['svcg_cycle', 'st', 'occr_default_per_state']].drop_duplicates()
        df_tmp['occr_default_per_state'] = df_tmp.groupby(['st'])['occr_default_per_state'].cumsum()
        df_tmp['occr_default_per_state_12_mon'] = df_tmp['occr_default_per_state'] - df_tmp.groupby(['st'])[
            'occr_default_per_state'].shift(12)
        df_tmp['occr_default_per_state_12_mon'] = df_tmp['occr_default_per_state_12_mon'].fillna(
            df_tmp['occr_default_per_state'])
        df1 = df1.drop('occr_default_per_state', 1)
        df1 = pd.merge(df_tmp, df1, on=['svcg_cycle', 'st'], how='right')

        df1 = df1.drop('paid_off', 1)
        df1 = df1.drop('default', 1)
        df1 = df1.drop('one_per_loan', 1)
        df1 = df1.drop('ones', 1)

        # ------------------ LOCAL FACTORS ------------------------

        return df1


    def create_ohc(self, data, exceptions):
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
                   'WI', 'WV', 'WY'],
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

        return data_ohc_all

    def one_hot_encoder(self, df, exceptions):

        for column in df:
            if column in exceptions:
                continue

            if not np.issubdtype(df[column].dtype, np.dtype(float).type) and not np.issubdtype(df[column].dtype,
                                                                                               np.dtype(int).type):
                df = pd.get_dummies(df, columns=[column])
        return df


if __name__ == "__main__":
    print "jkekr"



# LAST PAYMENT PCT
# df_A = df_A.sort_values(['svcg_cycle'], ascending=[False])
# df_cal = df_A.groupby(['id_loan']).nth(2)[['current_upb', 'orig_upb']]
#
# #     df_cal = df_A.groupby(['id_loan']).head(2).tail(1)[['id_loan', 'current_upb', 'orig_upb']]
# df_cal['last_payment_pct'] = df_cal['current_upb'] / df_cal['orig_upb']
# df_cal['id_loan'] = df_cal.index
# df_cal = df_cal.drop('current_upb', 1)
# df_cal = df_cal.drop('orig_upb', 1)
# df_A = pd.merge(df_cal, df_A, on='id_loan', how='right')
# df_A = df_A.sort_values(['last_payment_pct'], ascending=[False])