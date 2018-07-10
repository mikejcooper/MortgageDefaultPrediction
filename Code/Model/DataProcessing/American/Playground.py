

import time

from DataParser import DataParser
from DataProcessing import DataProcessing
from FeatureExtraction import FeatureExtraction

import pandas as pd

class Playground:
    """ A class that parses input data from file. """

    def __init__(self):

        # print df['id_loan'].value_counts()





        df_1_high = df.loc[df['id_loan'] == 'F199Q1159323']
        df_1_low = df.loc[df['id_loan'] == 'F199Q1059450']
        df_main = pd.concat((df_1_high, df_1_low))

        # df_main = df[:200]

        # Introduce new dataset - national mortgage rate
        df_nat_int_rt = DataParser().national_mortgage_rate()

        df_main = pd.merge(df_nat_int_rt, df_main, on='svcg_cycle', how='right')

        # Initialise new columns
        df_main.loc[:, 'time_since_origin'] = 1

        df_main.loc[:, 'pct_change'] = 0
        df_main.loc[:, 'crt_minus_nat_int_rt'] = 0

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

        for id_loan in df_main['id_loan'].unique():
            df_1 = df_main.loc[df_main['id_loan'] == id_loan]

            # Time since origin
            df_1['time_since_origin'] = df_1['time_since_origin'].cumsum()

            # ----------------------------------------------------------------------

            # Number of occurrences of current
            query = df_1.query("delq_sts == 0").index
            df_1.loc[query, 'occr_curr'] = 1
            df_1['occr_curr'] = df_1['occr_curr'].cumsum()

            # Number of occurrences of current in last 12 months
            loan_duration = df_1['id_loan'].value_counts().values
            if loan_duration[0] >= 12:
                df_1.loc[:, 'occr_curr_12_mon'] = df_1['occr_curr'] - df_1['occr_curr'].shift(12)
                df_1['occr_curr_12_mon'][:12] = df_1['occr_curr'][:12]
            else:
                df_1['occr_curr_12_mon'] = df_1['occr_curr']

            # ----------------------------------------------------------------------

            # Number of occurrences of 30 days delinquent
            query = df_1.query("delq_sts == 1").index
            df_1.loc[query, 'occr_30dd'] = 1
            df_1['occr_30dd'] = df_1['occr_30dd'].cumsum()

            # Number of occurrences of 30 days delinquent in last 12 months
            loan_duration = df_1['id_loan'].value_counts().values
            if loan_duration[0] >= 12:
                df_1.loc[:, 'occr_30dd_12_mon'] = df_1['occr_30dd'] - df_1['occr_30dd'].shift(12)
                df_1['occr_30dd_12_mon'][:12] = df_1['occr_30dd'][:12]
            else:
                df_1['occr_30dd_12_mon'] = df_1['occr_30dd']

            # ----------------------------------------------------------------------

            # Number of occurrences of 60 days delinquent
            query = df_1.query("delq_sts == 2").index
            df_1.loc[query, 'occr_60dd'] = 1
            df_1['occr_60dd'] = df_1['occr_60dd'].cumsum()

            # Number of occurrences of 60 days delinquent in last 12 months
            loan_duration = df_1['id_loan'].value_counts().values
            if loan_duration[0] >= 12:
                df_1.loc[:, 'occr_60dd_12_mon'] = df_1['occr_60dd'] - df_1['occr_60dd'].shift(12)
                df_1['occr_60dd_12_mon'][:12] = df_1['occr_60dd'][:12]
            else:
                df_1['occr_60dd_12_mon'] = df_1['occr_60dd']

            # ----------------------------------------------------------------------

            # Number of occurrences of 90+ days delinquent
            query = df_1.query("delq_sts > 2").index
            df_1.loc[query, 'occr_90dd'] = 1
            df_1['occr_90dd'] = df_1['occr_90dd'].cumsum()

            # Number of occurrences of 90+ days delinquent in last 12 months
            loan_duration = df_1['id_loan'].value_counts().values
            if loan_duration[0] >= 12:
                df_1.loc[:, 'occr_90dd_12_mon'] = df_1['occr_90dd'] - df_1['occr_90dd'].shift(12)
                df_1['occr_90dd_12_mon'][:12] = df_1['occr_90dd'][:12]
            else:
                df_1['occr_90dd_12_mon'] = df_1['occr_90dd']

            # ----------------------------------------------------------------------

            # Number of occurrences of Foreclosed
            query = df_1.query("label_month_0 == 4").index
            df_1.loc[query, 'occr_foreclosed'] = 1
            df_1['occr_foreclosed'] = df_1['occr_foreclosed'].cumsum()

            # Number of occurrences of Foreclosed in last 12 months
            loan_duration = df_1['id_loan'].value_counts().values
            if loan_duration[0] >= 12:
                df_1.loc[:, 'occr_foreclosed_12_mon'] = df_1['occr_foreclosed'] - df_1['occr_foreclosed'].shift(12)
                df_1['occr_foreclosed_12_mon'][:12] = df_1['occr_foreclosed'][:12]
            else:
                df_1['occr_foreclosed_12_mon'] = df_1['occr_foreclosed']

            # ----------------------------------------------------------------------

            # percentage change between last balance and current balance
            df_1['pct_change'] = (df_1['current_upb'] - df_1['current_upb'].shift(1)) / df_1['current_upb'].shift(1)
            df_1.loc[df_1['pct_change'] == -1.0, 'pct_change'] = 0
            df_1 = df_1.fillna(0)

            # ----------------------------------------------------------------------

            # Current interest rate − national mortgage rate
            df_1['crt_minus_nat_int_rt'] = df_1['current_int_rt'] - df_1['nat_int_rt']

            # ----------------------------------------------------------------------
            # ----------------------------------------------------------------------

            # Set main dataframe to local values for current loan
            df_main.loc[df_main['id_loan'] == id_loan] = df_1.loc[df_1['id_loan'] == id_loan]

        print df_main[['time_since_origin', 'current_upb', 'pct_change']]











            # def __init__(self):
    #     """ Example of docstring on the __init__ method.  """
    #     A = []
    #     B = []
    #     C = []
    #     B = B + ['Other servicers', 'CHASEMTGECO', 'NATLCITYMTGECO', 'FIFTHTHIRDBANK'
    #                                                                  'GMACMTGECORP', 'FTMTGESERVICES,INC',
    #              'WELLSFARGOHOMEMORTGA'
    #              'CHASEMANHATTANMTGECO', 'SUNTRUSTMORTGAGE,INC', 'HOMESIDELENDING,INC'
    #                                                              'BAMORTGAGE,LLC', 'CITIMORTGAGE,INC',
    #              'PRINCIPALRESIDENTIAL'
    #              'BANKOFAMERICA,NA', 'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC'
    #                                                          'COUNTRYWIDE', 'WELLSFARGOBANK,NA', 'CHASEHOMEFINANCELLC'
    #                                                                                              'JPMORGANCHASEBANK,NA']
    #     C = C + ['Other sellers', 'FT MORTGAGE COMPANIE', 'OLD KENT MORTGAGE CO'
    #                                                       'NATIONAL CITY MORTGA', 'FIRST UNION CAPITAL',
    #              'FLEET MORTGAGE CORPO'
    #              'CROSSLAND MORTGAGE C', 'GMAC MORTGAGE CORPOR', 'ACCUBANC MORTGAGE CO'
    #                                                              'NORWEST MORTGAGE, IN', 'FLAGSTAR BANK, FSB',
    #              'NATIONSBANC MORTGAGE'
    #              'HOMESIDE LENDING, IN', 'RESOURCE BANCSHARES', 'PRINCIPAL RESIDENTIA'
    #                                                             'CHASE MANHATTAN MORT', 'NAMCO ASSET MANAGEME',
    #              'BANKAMERICA MORTGAGE'
    #              'PNC MORTGAGE CORPORA', 'G N MORTGAGE CORPORA', 'WASHINGTON MUTUAL BA'
    #                                                              'STANDARD FEDERAL BAN' "BISHOP'S GATE RESIDE" 'NATIONSBANK, N.A.'
    #                                                              'COUNTRYWIDE HOME LOA']
    #     A = A + ['PA', 'WV', 'OH', 'WI', 'MA', 'AZ', 'IL', 'FL', 'GA', 'MO', 'MI', 'CA', 'NM', 'IA'
    #                                                                                            'IN', 'CO', 'WA', 'CT',
    #              'VA', 'KS', 'TX', 'NY', 'AL', 'MD', 'ID', 'RI', 'LA', 'PR'
    #                                                                    'SD', 'NC', 'SC', 'MN', 'NJ', 'NV', 'HI', 'OR',
    #              'UT', 'NH', 'TN', 'OK', 'KY', 'VT'
    #                                            'NE', 'ME', 'MT', 'DE', 'DC', 'GU', 'AK', 'AR', 'WY', 'ND']
    #     B = B + ['Other servicers', 'NATLCITYMTGECO', 'CHASEMTGECO', 'GMACMTGECORP'
    #                                                                  'CHASEMANHATTANMTGECO', 'WELLSFARGOHOMEMORTGA',
    #              'BANKOFAMERICA,NA'
    #              'BAMORTGAGE,LLC', 'HOMESIDELENDING,INC', 'PRINCIPALRESIDENTIAL'
    #                                                       'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC',
    #              'CENDANTMTGECORPORATI'
    #              'COUNTRYWIDE', 'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers', 'NATIONAL CITY MORTGA', 'OLD KENT MORTGAGE CO'
    #                                                       'CROSSLAND MORTGAGE C', 'CHASE MANHATTAN MORT',
    #              'FT MORTGAGE COMPANIE'
    #              'ACCUBANC MORTGAGE CO', 'NORWEST MORTGAGE, IN', 'G N MORTGAGE CORPORA'
    #                                                              'BANK OF AMERICA, N.A', 'NATIONSBANC MORTGAGE',
    #              'FLAGSTAR BANK, FSB'
    #              'PRINCIPAL RESIDENTIA' "BISHOP'S GATE RESIDE" 'GE CAPITAL MORTGAGE'
    #              'FIRSTAR BANK, N.A.', 'PNC MORTGAGE CORPORA', 'ABN AMRO MORTGAGE GR'
    #                                                            'COUNTRYWIDE HOME LOA']
    #     A = A + ['OH', 'WI', 'SC', 'MN', 'NY', 'AZ', 'MO', 'OK', 'IL', 'MI', 'FL', 'PA', 'CA', 'IN'
    #                                                                                            'TX', 'GA', 'NH', 'TN',
    #              'CO', 'UT', 'DE', 'AL', 'WV', 'MD', 'CT', 'NC', 'MA', 'ME'
    #                                                                    'OR', 'VA', 'KS', 'KY', 'NJ', 'ID', 'WA', 'IA',
    #              'NM', 'MT', 'ND', 'NV', 'LA', 'AR'
    #                                            'RI', 'NE', 'MS', 'HI', 'SD', 'VT', 'AK', 'DC', 'WY', 'GU']
    #     B = B + ['Other servicers', 'CHASEMTGECO', 'NATLCITYMTGECO', 'GMACMTGECORP'
    #                                                                  'WELLSFARGOHOMEMORTGA', 'BANKOFAMERICA,NA',
    #              'PRINCIPALRESIDENTIAL'
    #              'BRANCHBANKING&TRUSTC', 'HOMESIDELENDING,INC', 'FTMTGESERVICES,INC'
    #                                                             'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC',
    #              'COUNTRYWIDE'
    #              'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORP'
    #                                                                  'CHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC',
    #              'BANKOFAMERICA,NA'
    #              'FLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIAL'
    #                                                          'BISHOPSGATERESIDENTI', 'FTMTGECOMPANIES',
    #              'GECAPITALMTGESERVICE'
    #              'FIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC'
    #                                                        'COUNTRYWIDE']
    #     A = A + ['WI', 'OH', 'CO', 'NY', 'WV', 'SC', 'GA', 'MI', 'PA', 'OK', 'AZ', 'CA', 'NC', 'NJ'
    #                                                                                            'TX', 'KS', 'FL', 'CT',
    #              'OR', 'WA', 'IL', 'NE', 'RI', 'DE', 'MD', 'MO', 'MN', 'TN'
    #                                                                    'KY', 'NM', 'NH', 'MA', 'AR', 'NV', 'VA', 'IA',
    #              'AK', 'IN', 'AL', 'UT', 'MT', 'VT'
    #                                            'ID', 'GU', 'ME', 'HI', 'MS', 'WY', 'LA', 'SD', 'ND', 'DC', 'VI']
    #     B = B + ['Other servicers', 'CHASEMTGECO', 'NATLCITYMTGECO', 'GMACMTGECORP'
    #                                                                  'WELLSFARGOHOMEMORTGA', 'BANKOFAMERICA,NA',
    #              'PRINCIPALRESIDENTIAL'
    #              'BRANCHBANKING&TRUSTC', 'HOMESIDELENDING,INC', 'FTMTGESERVICES,INC'
    #                                                             'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC',
    #              'COUNTRYWIDE'
    #              'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORP'
    #                                                                  'CHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC',
    #              'BANKOFAMERICA,NA'
    #              'FLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIAL'
    #                                                          'BISHOPSGATERESIDENTI', 'FTMTGECOMPANIES',
    #              'GECAPITALMTGESERVICE'
    #              'FIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC'
    #                                                        'COUNTRYWIDE']
    #     A = A + ['WI', 'OH', 'CO', 'NY', 'WV', 'SC', 'GA', 'MI', 'PA', 'OK', 'AZ', 'CA', 'NC', 'NJ'
    #                                                                                            'TX', 'KS', 'FL', 'CT',
    #              'OR', 'WA', 'IL', 'NE', 'RI', 'DE', 'MD', 'MO', 'MN', 'TN'
    #                                                                    'KY', 'NM', 'NH', 'MA', 'AR', 'NV', 'VA', 'IA',
    #              'AK', 'IN', 'AL', 'UT', 'MT', 'VT'
    #                                            'ID', 'GU', 'ME', 'HI', 'MS', 'WY', 'LA', 'SD', 'ND', 'DC', 'VI']
    #     B = B + ['Other servicers', 'NATLCITYMTGECO', 'WASHINGTONMUTUALHOME', 'CHASEMTGECO'
    #                                                                           'GMACMTGECORP', 'WASHINGTONMUTUALBANK',
    #              'BANKOFAMERICA,NA'
    #              'HOMESIDELENDING,INC', 'WELLSFARGOHOMEMORTGA', 'BRANCHBANKING&TRUSTC'
    #                                                             'FTMTGESERVICES,INC', 'PRINCIPALRESIDENTIAL',
    #              'ABNAMROMTGEGROUP,INC'
    #              'CENDANTMTGECORPORATI', 'COUNTRYWIDE', 'FIFTHTHIRDBANK', 'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORP'
    #                                                                  'CHASEMANHATTANMTGECO', 'BANKOFAMERICA,NA',
    #              'FLAGSTARBANK,FSB'
    #              'WELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                        'BISHOPSGATERESIDENTI', 'PRINCIPALRESIDENTIAL',
    #              'FIRSTHORIZONHOMELOAN'
    #              'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE'
    #                                                              'FIFTHTHIRDBANK']
    #     A = A + ['WI', 'OH', 'MA', 'PA', 'SC', 'NY', 'MO', 'MI', 'TX', 'CA', 'DC', 'ID', 'VA', 'NJ'
    #                                                                                            'FL', 'NC', 'MS', 'MD',
    #              'UT', 'GA', 'IN', 'IA', 'CT', 'KY', 'KS', 'OR', 'CO', 'AZ'
    #                                                                    'MN', 'NV', 'WA', 'TN', 'MT', 'SD', 'HI', 'AL',
    #              'IL', 'NE', 'PR', 'NH', 'AR', 'AK'
    #                                            'LA', 'OK', 'NM', 'VT', 'ME', 'ND', 'RI', 'DE', 'WV', 'GU', 'WY']
    #     B = B + ['Other servicers', 'FIFTHTHIRDBANK', 'NATLCITYMTGECO', 'OLDKENTMTGECO'
    #                                                                     'CHASEMTGECO', 'WASHINGTONMUTUALHOME',
    #              'GMACMTGECORP', 'COUNTRYWIDE'
    #                              'BANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGA', 'PRINCIPALRESIDENTIAL'
    #                                                                          'BRANCHBANKING&TRUSTC',
    #              'WASHINGTONMUTUALBANK', 'CENDANTMTGECORPORATI'
    #                                      'ABNAMROMTGEGROUP,INC', 'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers', 'NATLCITYMTGECO', 'OLDKENTMTGECO', 'CHASEMANHATTANMTGECO'
    #                                                                  'COUNTRYWIDE', 'BANKOFAMERICA,NA',
    #              'WELLSFARGOHOMEMORTGA'
    #              'FLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'CROSSLANDMTGECORP'
    #                                                          'PRINCIPALRESIDENTIAL', 'BISHOPSGATERESIDENTI',
    #              'PNCMTGECORPOFAMERICA'
    #              'FIRSTARBANK,NA', 'ABNAMROMTGEGROUP,INC']
    #     A = A + ['WI', 'IN', 'PA', 'OH', 'KY', 'WV', 'MA', 'SC', 'NY', 'ID', 'TX', 'MO', 'IL', 'MI'
    #                                                                                            'CA', 'CO', 'VA', 'NJ',
    #              'OK', 'FL', 'GA', 'TN', 'AZ', 'UT', 'MD', 'WA', 'OR', 'MN'
    #                                                                    'NC', 'NH', 'IA', 'AR', 'AK', 'KS', 'ME', 'NV',
    #              'SD', 'NE', 'AL', 'RI', 'ND', 'NM'
    #                                            'HI', 'VT', 'CT', 'LA', 'MS', 'DE', 'WY', 'DC', 'GU', 'MT']
    #     B = B + ['Other servicers', 'OLDKENTMTGECO', 'FIFTHTHIRDBANK', 'NATLCITYMTGECO'
    #                                                                    'CHASEMTGECO', 'GMACMTGECORP', 'COUNTRYWIDE',
    #              'PRINCIPALRESIDENTIAL'
    #              'BANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGA', 'BRANCHBANKING&TRUSTC'
    #                                                          'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC']
    #     C = C + ['Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECO'
    #                                                                  'COUNTRYWIDE', 'BANKOFAMERICA,NA',
    #              'FLAGSTARBANK,FSB'
    #              'WELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                        'PRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN',
    #              'BISHOPSGATERESIDENTI'
    #              'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC']
    #     A = A + ['WI', 'AZ', 'IN', 'OH', 'NY', 'MI', 'KY', 'MO', 'CA', 'NV', 'IL', 'MD', 'MA', 'NC'
    #                                                                                            'TN', 'ID', 'FL', 'SC',
    #              'NJ', 'VA', 'GA', 'TX', 'PA', 'CO', 'UT', 'AR', 'WA', 'OR'
    #                                                                    'KS', 'IA', 'WY', 'NH', 'VT', 'DE', 'NE', 'MN',
    #              'MT', 'HI', 'LA', 'CT', 'OK', 'AL'
    #                                            'ND', 'NM', 'MS', 'WV', 'DC', 'RI']
    #     B = B + ['Other servicers', 'OLDKENTMTGECO', 'FIFTHTHIRDBANK', 'NATLCITYMTGECO'
    #                                                                    'CHASEMTGECO', 'GMACMTGECORP', 'COUNTRYWIDE',
    #              'PRINCIPALRESIDENTIAL'
    #              'BANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGA', 'BRANCHBANKING&TRUSTC'
    #                                                          'WASHINGTONMUTUALBANK', 'ABNAMROMTGEGROUP,INC']
    #     C = C + ['Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECO'
    #                                                                  'COUNTRYWIDE', 'BANKOFAMERICA,NA',
    #              'FLAGSTARBANK,FSB'
    #              'WELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                        'PRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN',
    #              'BISHOPSGATERESIDENTI'
    #              'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC']
    #     A = A + ['WI', 'AZ', 'IN', 'OH', 'NY', 'MI', 'KY', 'MO', 'CA', 'NV', 'IL', 'MD', 'MA', 'NC'
    #                                                                                            'TN', 'ID', 'FL', 'SC',
    #              'NJ', 'VA', 'GA', 'TX', 'PA', 'CO', 'UT', 'AR', 'WA', 'OR'
    #                                                                    'KS', 'IA', 'WY', 'NH', 'VT', 'DE', 'NE', 'MN',
    #              'MT', 'HI', 'LA', 'CT', 'OK', 'AL'
    #                                            'ND', 'NM', 'MS', 'WV', 'DC', 'RI']
    #     B = B + ['Other servicers', 'PROVIDENTFUNDINGASSO', 'FIFTHTHIRDBANK'
    #                                                         'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKER',
    #              'WELLSFARGOBANK,NA'
    #              'CITIMORTGAGE,INC', 'USBANKNA', 'NATLCITYMTGECO', 'PRINCIPALRESIDENTIAL'
    #                                                                'ABNAMROMTGEGROUP,INC', 'CHASEMTGECO',
    #              'WASHINGTONMUTUALBANK'
    #              'SUNTRUSTMORTGAGE,INC', 'WELLSFARGOHOMEMORTGA']
    #     C = C + ['Other sellers', 'PROVIDENTFUNDINGASSO', 'TAYLOR,BEAN&WHITAKER'
    #                                                       'ABNAMROMTGEGROUP,INC', 'PRINCIPALRESIDENTIAL',
    #              'WELLSFARGOHOMEMORTGA'
    #              'FLAGSTARBANK,FSB', 'SUNTRUSTMORTGAGE,INC']
    #     A = A + ['MN', 'MI', 'GA', 'OK', 'OH', 'IL', 'OR', 'NY', 'PA', 'IN', 'WA', 'SC', 'FL', 'MT'
    #                                                                                            'AR', 'WI', 'KY', 'NC',
    #              'VT', 'NV', 'MA', 'NH', 'CA', 'ID', 'NJ', 'UT', 'MD', 'TN'
    #                                                                    'TX', 'DE', 'VA', 'KS', 'NE', 'MO', 'IA', 'ME',
    #              'WV', 'CO', 'AL', 'AZ', 'ND', 'LA'
    #                                            'CT', 'RI', 'AK', 'SD', 'NM', 'WY', 'HI']
    #     B = B + ['Other servicers', 'FIFTHTHIRDBANK', 'BRANCHBANKING&TRUSTC'
    #                                                   'WELLSFARGOBANK,NA']
    #     C = C + ['Other sellers']
    #     A = A + ['MI', 'NH', 'MN', 'VT', 'IL', 'WI', 'IN', 'MO', 'NY', 'KY', 'OH', 'GA', 'ME', 'PA'
    #                                                                                            'OR', 'RI', 'OK', 'FL',
    #              'TN', 'MA', 'SC', 'NE', 'KS', 'DE', 'IA', 'CT', 'NJ', 'ID'
    #                                                                    'NC', 'WV', 'MD', 'NV', 'AL', 'WA', 'TX', 'AR',
    #              'CA', 'VA', 'MT', 'LA', 'WY', 'CO'
    #                                            'SD', 'NM', 'UT', 'AZ']
    #     B = B + ['Other servicers', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                         'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers']
    #     A = A + ['IN', 'WI', 'MN', 'IL', 'VT', 'MI', 'OH', 'KY', 'MO', 'NY', 'KS', 'MA', 'IA', 'ME'
    #                                                                                            'NE', 'TX', 'NH', 'FL',
    #              'SC', 'GA', 'NJ', 'VA', 'OK', 'PA', 'OR', 'CT', 'NC', 'CA'
    #                                                                    'MD', 'SD', 'WA', 'NV', 'TN', 'AK', 'AZ', 'ID',
    #              'DE', 'WV', 'AR', 'CO', 'AL', 'GU']
    #     B = B + ['Other servicers', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                         'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers']
    #     A = A + ['IN', 'WI', 'MN', 'IL', 'VT', 'MI', 'OH', 'KY', 'MO', 'NY', 'KS', 'MA', 'IA', 'ME'
    #                                                                                            'NE', 'TX', 'NH', 'FL',
    #              'SC', 'GA', 'NJ', 'VA', 'OK', 'PA', 'OR', 'CT', 'NC', 'CA'
    #                                                                    'MD', 'SD', 'WA', 'NV', 'TN', 'AK', 'AZ', 'ID',
    #              'DE', 'WV', 'AR', 'CO', 'AL', 'GU']
    #     B = B + ['Other servicers', 'WELLSFARGOBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                      'FIFTHTHIRDBANK', 'PNCBANK,NATL', 'NATLCITYMTGECO',
    #              'PNCMTGESERVICES,INC'
    #              'CITIMORTGAGE,INC']
    #     C = C + ['Other sellers']
    #     A = A + ['NY', 'MN', 'NH', 'WI', 'WA', 'VT', 'MA', 'IL', 'FL', 'AZ', 'IA', 'MI', 'OH', 'TX'
    #                                                                                            'KS', 'KY', 'TN', 'NC',
    #              'IN', 'PA', 'NJ', 'CT', 'MO', 'ME', 'SC', 'CO', 'DE', 'NE'
    #                                                                    'GA', 'OK', 'AR', 'MD', 'RI', 'VA', 'CA', 'MT',
    #              'OR', 'HI', 'WV', 'ID', 'MS', 'LA'
    #                                            'UT', 'SD', 'AL', 'NV', 'NM']
    #     B = B + ['Other servicers', 'WELLSFARGOBANK,NA', 'CITIMORTGAGE,INC'
    #                                                      'BRANCHBANKING&TRUSTC', 'USBANKNA', 'FIFTHTHIRDBANK',
    #              'PNCBANK,NATL'
    #              'ABNAMROMTGEGROUP,INC', 'NATLCITYMTGECO', 'PNCMTGESERVICES,INC']
    #     C = C + ['Other sellers']
    #     A = A + ['CA', 'MA', 'MN', 'NH', 'OH', 'NJ', 'IL', 'NY', 'WI', 'VT', 'WA', 'PA', 'TX', 'IN'
    #                                                                                            'MO', 'IA', 'MD', 'GA',
    #              'MI', 'KY', 'KS', 'SC', 'CT', 'TN', 'UT', 'AK', 'ME', 'NE'
    #                                                                    'FL', 'OK', 'CO', 'OR', 'AZ', 'DE', 'ID', 'LA',
    #              'NM', 'VA', 'NC', 'HI', 'WV', 'NV'
    #                                            'AR', 'RI', 'PR', 'MT', 'AL', 'MS', 'SD', 'DC']
    #     B = B + ['Other servicers', 'JPMORGANCHASEBANK,NA', 'WELLSFARGOBANK,NA'
    #                                                         'ABNAMROMTGEGROUP,INC', 'CITIMORTGAGE,INC',
    #              'PNCMTGESERVICES,INC'
    #              'USBANKNA', 'PNCBANK,NATL', 'NATLCITYMTGECO', 'COUNTRYWIDE'
    #                                                            'CHASEHOMEFINANCELLC', 'CHASEMANHATTANMTGECO']
    #     C = C + ['Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIAL'
    #                                              'ABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA',
    #              'USBANKNA']
    #     A = A + ['OK', 'MA', 'WI', 'AK', 'ME', 'NH', 'CO', 'AZ', 'IN', 'IL', 'KS', 'MN', 'OH', 'IA'
    #                                                                                            'NY', 'MI', 'SC', 'VT',
    #              'GA', 'PR', 'UT', 'MO', 'VA', 'WV', 'ID', 'AL', 'OR', 'WA'
    #                                                                    'PA', 'TX', 'NM', 'NC', 'NE', 'KY', 'DE', 'CA',
    #              'FL', 'TN', 'MT', 'CT', 'HI', 'RI'
    #                                            'AR', 'NV', 'NJ', 'MD', 'ND', 'LA', 'GU', 'MS', 'WY', 'DC', 'SD']
    #     B = B + ['Other servicers', 'JPMORGANCHASEBANK,NA', 'WELLSFARGOBANK,NA'
    #                                                         'ABNAMROMTGEGROUP,INC', 'CITIMORTGAGE,INC',
    #              'PNCMTGESERVICES,INC'
    #              'USBANKNA', 'PNCBANK,NATL', 'NATLCITYMTGECO', 'COUNTRYWIDE'
    #                                                            'CHASEHOMEFINANCELLC', 'CHASEMANHATTANMTGECO']
    #     C = C + ['Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIAL'
    #                                              'ABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA',
    #              'USBANKNA']
    #     A = A + ['OK', 'MA', 'WI', 'AK', 'ME', 'NH', 'CO', 'AZ', 'IN', 'IL', 'KS', 'MN', 'OH', 'IA'
    #                                                                                            'NY', 'MI', 'SC', 'VT',
    #              'GA', 'PR', 'UT', 'MO', 'VA', 'WV', 'ID', 'AL', 'OR', 'WA'
    #                                                                    'PA', 'TX', 'NM', 'NC', 'NE', 'KY', 'DE', 'CA',
    #              'FL', 'TN', 'MT', 'CT', 'HI', 'RI'
    #                                            'AR', 'NV', 'NJ', 'MD', 'ND', 'LA', 'GU', 'MS', 'WY', 'DC', 'SD']
    #     B = B + ['WELLSFARGOBANK,NA', 'Other servicers', 'USBANKNA', 'JPMORGANCHASEBANK,NA'
    #                                                                  'NATLCITYMTGECO', 'PNCBANK,NATL',
    #              'PNCMTGESERVICES,INC'
    #              'CHASEHOMEFINANCELLC', 'CITIMORTGAGE,INC', 'FIFTHTHIRDBANK'
    #                                                         'BRANCHBANKING&TRUSTC', 'NATIONSTARMTGELLC',
    #              'ABNAMROMTGEGROUP,INC']
    #     C = C + ['WELLSFARGOBANK', 'Other sellers', 'TAYLOR,BEAN&WHITAKER'
    #                                                    'FIFTHTHIRDBANK']
    #     A = A + ['PA', 'VA', 'MD', 'GA', 'WV', 'WI', 'FL', 'WA', 'NC', 'CT', 'RI', 'CO', 'MI', 'NY'
    #                                                                                            'MO', 'AZ', 'IN', 'HI',
    #              'MN', 'ME', 'KS', 'IA', 'VT', 'OR', 'IL', 'NJ', 'MA', 'NE'
    #                                                                    'KY', 'SC', 'NH', 'OK', 'TX', 'CA', 'OH', 'TN',
    #              'ND', 'AK', 'ID', 'AL', 'LA', 'UT'
    #                                            'NM', 'MS', 'AR', 'MT', 'DE', 'NV', 'GU']
    #     B = B + ['Other servicers', 'JPMORGANCHASEBANK,NA', 'USBANKNA', 'PNCBANK,NATL'
    #                                                                     'PNCMTGESERVICES,INC', 'NATLCITYMTGECO',
    #              'WELLSFARGOBANK,NA'
    #              'BRANCHBANKING&TRUSTC', 'NATIONSTARMTGELLC', 'CHASEHOMEFINANCELLC'
    #                                                           'CITIMORTGAGE,INC', 'COUNTRYWIDE', 'ABNAMROMTGEGROUP,INC']
    #     C = C + ['Other sellers', 'TAYLOR,BEAN&WHITAKER', 'CHASEMANHATTANMTGECO'
    #                                                       'BRANCHBANKING&TRUSTC']
    #     A = A + ['WI', 'FL', 'WA', 'ME', 'IN', 'PA', 'OR', 'KY', 'MN', 'CO', 'OH', 'IL', 'VA', 'KS'
    #                                                                                            'UT', 'GA', 'NE', 'MO',
    #              'NY', 'TX', 'IA', 'MI', 'ND', 'NC', 'DE', 'CT', 'CA', 'MD'
    #                                                                    'NH', 'AL', 'SD', 'NJ', 'OK', 'WV', 'MA', 'ID',
    #              'AZ', 'SC', 'RI', 'HI', 'WY', 'MT'
    #                                            'TN', 'VT', 'NM', 'AK', 'NV', 'GU', 'LA', 'AR', 'MS', 'DC', 'PR']
    #     B = B + ['Other servicers', 'JPMORGANCHASEBANK,NA', 'USBANKNA', 'PNCBANK,NATL'
    #                                                                     'PNCMTGESERVICES,INC', 'WELLSFARGOBANK,NA',
    #              'NATLCITYMTGECO'
    #              'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKER', 'CITIMORTGAGE,INC'
    #                                                              'NATIONSTARMTGELLC', 'CHASEHOMEFINANCELLC',
    #              'ABNAMROMTGEGROUP,INC']
    #     C = C + ['Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA']
    #     A = A + ['ME', 'IL', 'CA', 'WA', 'OH', 'MD', 'KS', 'WI', 'MN', 'CO', 'FL', 'KY', 'SC', 'NY'
    #                                                                                            'AL', 'IN', 'GA', 'MI',
    #              'VA', 'TX', 'MO', 'IA', 'CT', 'ND', 'NE', 'PA', 'OR', 'NC'
    #                                                                    'UT', 'NJ', 'AZ', 'OK', 'RI', 'MA', 'NH', 'WY',
    #              'SD', 'DE', 'WV', 'MT', 'TN', 'ID'
    #                                            'HI', 'VT', 'NM', 'AK', 'AR', 'NV', 'PR', 'LA', 'MS', 'DC', 'GU']
    #     B = B + ['Other servicers', 'JPMORGANCHASEBANK,NA', 'USBANKNA', 'PNCBANK,NATL'
    #                                                                     'PNCMTGESERVICES,INC', 'WELLSFARGOBANK,NA',
    #              'NATLCITYMTGECO'
    #              'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKER', 'CITIMORTGAGE,INC'
    #                                                              'NATIONSTARMTGELLC', 'CHASEHOMEFINANCELLC',
    #              'ABNAMROMTGEGROUP,INC']
    #     C = C + ['Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA']
    #     A = A + ['ME', 'IL', 'CA', 'WA', 'OH', 'MD', 'KS', 'WI', 'MN', 'CO', 'FL', 'KY', 'SC', 'NY'
    #                                                                                            'AL', 'IN', 'GA', 'MI',
    #              'VA', 'TX', 'MO', 'IA', 'CT', 'ND', 'NE', 'PA', 'OR', 'NC'
    #                                                                    'UT', 'NJ', 'AZ', 'OK', 'RI', 'MA', 'NH', 'WY',
    #              'SD', 'DE', 'WV', 'MT', 'TN', 'ID'
    #                                            'HI', 'VT', 'NM', 'AK', 'AR', 'NV', 'PR', 'LA', 'MS', 'DC', 'GU']
    #     B = B + ['WELLSFARGOBANK,NA', 'PNCMTGESERVICES,INC', 'Other servicers', 'USBANKNA'
    #                                                                             'NATLCITYMTGECO', 'PNCBANK,NATL',
    #              'GMACMORTGAGE,LLC', 'NATIONSTARMTGELLC'
    #                                  'BACHOMELOANSERVICING', 'COUNTRYWIDE', 'BANKOFAMERICA,NA'
    #                                                                         'JPMORGANCHASEBANK,NA', 'CITIMORTGAGE,INC',
    #              'PROVIDENTFUNDINGASSO'
    #              'ABNAMROMTGEGROUP,INC', 'BRANCHBANKING&TRUSTC']
    #     C = C + ['Other sellers', 'GMACMTGECORP', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKER'
    #                                                              'PROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC',
    #              'CHASEHOMEFINANCELLC'
    #              'USBANKNA', 'FIFTHTHIRDBANK', 'ABNAMROMTGEGROUP,INC']
    #     A = A + ['CA', 'IL', 'FL', 'MN', 'NE', 'IN', 'IA', 'OR', 'MO', 'NY', 'GA', 'WI', 'CT', 'KY'
    #                                                                                            'OH', 'WA', 'MI', 'VA',
    #              'SC', 'TX', 'KS', 'DE', 'NC', 'ND', 'RI', 'ME', 'NJ', 'OK'
    #                                                                    'CO', 'TN', 'NH', 'DC', 'PA', 'HI', 'MT', 'WV',
    #              'MA', 'MD', 'SD', 'ID', 'AL', 'UT'
    #                                            'WY', 'VT', 'AK', 'AZ', 'LA', 'PR', 'NV', 'NM', 'AR', 'MS', 'GU']
    #     B = B + ['WELLSFARGOBANK,NA', 'Other servicers', 'USBANKNA', 'NATLCITYMTGECO'
    #                                                                  'PNCMTGESERVICES,INC', 'PNCBANK,NATL',
    #              'COUNTRYWIDE', 'BANKOFAMERICA,NA'
    #                             'BACHOMELOANSERVICING', 'JPMORGANCHASEBANK,NA', 'NATIONSTARMTGELLC'
    #                                                                             'OCWENLOANSERVICING,L',
    #              'CITIMORTGAGE,INC', 'ABNAMROMTGEGROUP,INC']
    #     C = C + ['WELLSFARGOCANKCNA', 'Other sellers', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKER'
    #                                                                   'ABNAMROMTGEGROUP,INC', 'USBANKNA',
    #              'FLAGSTARBANK,FSB']
    #     A = A + ['TX', 'IN', 'PA', 'NJ', 'WA', 'MI', 'MA', 'UT', 'FL', 'AZ', 'CA', 'MN', 'OR', 'NC'
    #                                                                                            'MT', 'AR', 'MD', 'MO',
    #              'IL', 'CO', 'SD', 'NH', 'NV', 'WY', 'IA', 'OH', 'CT', 'SC'
    #                                                                    'KS', 'WV', 'KY', 'ME', 'GA', 'WI', 'NY', 'NE',
    #              'RI', 'ND', 'DE', 'OK', 'VA', 'AL'
    #                                            'AK', 'HI', 'TN', 'VT', 'LA', 'DC', 'ID', 'NM', 'MS']
    #     B = B + ['Other servicers', 'USBANKNA', 'PNCBANK,NATL', 'CITIMORTGAGE,INC'
    #                                                             'BACHOMELOANSERVICING', 'BANKOFAMERICA,NA',
    #              'WELLSFARGOBANK,NA'
    #              'COUNTRYWIDE', 'JPMORGANCHASEBANK,NA', 'PNCMTGESERVICES,INC'
    #                                                     'NATIONSTARMTGELLC', 'GMACMORTGAGE,LLC', 'TAYLOR,BEAN&WHITAKER'
    #                                                                                              'WASHINGTONMUTUALBANK']
    #     C = C + ['Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORP'
    #                                                                      'TAYLOR,BEAN&WHITAKER', 'USBANKNA',
    #              'WASHINGTONMUTUALBANK'
    #              'FLAGSTARBANK,FSB']
    #     A = A + ['MI', 'IL', 'WA', 'IA', 'KY', 'GA', 'KS', 'OH', 'MN', 'FL', 'ND', 'TX', 'IN', 'WI'
    #                                                                                            'NE', 'CO', 'MO', 'MA',
    #              'VA', 'ME', 'RI', 'SC', 'NY', 'CA', 'AK', 'NC', 'CT', 'MD'
    #                                                                    'OR', 'NH', 'DE', 'NJ', 'MT', 'OK', 'PA', 'WV',
    #              'WY', 'HI', 'AL', 'MS', 'SD', 'TN'
    #                                            'ID', 'LA', 'VT', 'GU', 'UT', 'AZ', 'NM', 'AR', 'NV', 'DC', 'VI']
    #     B = B + ['Other servicers', 'USBANKNA', 'PNCBANK,NATL', 'CITIMORTGAGE,INC'
    #                                                             'BACHOMELOANSERVICING', 'BANKOFAMERICA,NA',
    #              'WELLSFARGOBANK,NA'
    #              'COUNTRYWIDE', 'JPMORGANCHASEBANK,NA', 'PNCMTGESERVICES,INC'
    #                                                     'NATIONSTARMTGELLC', 'GMACMORTGAGE,LLC', 'TAYLOR,BEAN&WHITAKER'
    #                                                                                              'WASHINGTONMUTUALBANK']
    #     C = C + ['Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORP'
    #                                                                      'TAYLOR,BEAN&WHITAKER', 'USBANKNA',
    #              'WASHINGTONMUTUALBANK'
    #              'FLAGSTARBANK,FSB']
    #     A = A + ['MI', 'IL', 'WA', 'IA', 'KY', 'GA', 'KS', 'OH', 'MN', 'FL', 'ND', 'TX', 'IN', 'WI'
    #                                                                                            'NE', 'CO', 'MO', 'MA',
    #              'VA', 'ME', 'RI', 'SC', 'NY', 'CA', 'AK', 'NC', 'CT', 'MD'
    #                                                                    'OR', 'NH', 'DE', 'NJ', 'MT', 'OK', 'PA', 'WV',
    #              'WY', 'HI', 'AL', 'MS', 'SD', 'TN'
    #                                            'ID', 'LA', 'VT', 'GU', 'UT', 'AZ', 'NM', 'AR', 'NV', 'DC', 'VI']
    #     B = B + ['Other servicers', 'USBANKNA', 'CITIMORTGAGE,INC', 'BACHOMELOANSERVICING'
    #                                                                 'NATIONSTARMTGELLC', 'BANKOFAMERICA,NA',
    #              'COUNTRYWIDE'
    #              'BRANCHBANKING&TRUSTC', 'JPMORGANCHASEBANK,NA', 'FIFTHTHIRDBANK'
    #                                                              'WELLSFARGOBANK,NA', 'WASHINGTONMUTUALBANK',
    #              'TAYLOR,BEAN&WHITAKER']
    #     C = C + ['Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'USBANKNA'
    #                                                                      'BRANCHBANKING&TRUSTC', 'SOVEREIGNBANK',
    #              'FIFTHTHIRDBANK'
    #              'WELLSFARGOBANK,NA', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER'
    #                                                           'CHASEHOMEFINANCELLC']
    #     A = A + ['VA', 'WI', 'WY', 'WA', 'MN', 'CO', 'ME', 'NY', 'IA', 'CA', 'KY', 'IL', 'FL', 'MO'
    #                                                                                            'IN', 'NJ', 'MI', 'OK',
    #              'CT', 'PA', 'OH', 'AK', 'ND', 'NC', 'GA', 'AZ', 'NH', 'NE'
    #                                                                    'KS', 'TX', 'MA', 'RI', 'WV', 'OR', 'SC', 'TN',
    #              'MD', 'AL', 'UT', 'MT', 'SD', 'ID'
    #                                            'DE', 'VT', 'GU', 'HI', 'NM', 'LA', 'NV', 'DC', 'AR', 'MS']
    #     B = B + ['USBANKNA', 'Other servicers', 'BACHOMELOANSERVICING', 'CITIMORTGAGE,INC'
    #                                                                     'BANKOFAMERICA,NA', 'COUNTRYWIDE',
    #              'NATIONSTARMTGELLC'
    #              'PROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'JPMORGANCHASEBANK,NA'
    #                                                              'FIFTHTHIRDBANK', 'GMACMORTGAGE,LLC',
    #              'WELLSFARGOBANK,NA'
    #              'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE']
    #     C = C + ['Other sellers', 'COUNTRYWIDE', 'ABNAMROMTGEGROUP,INC'
    #                                              'PROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANK'
    #                                                                                              'GMACMTGECORP',
    #              'TAYLOR,BEAN&WHITAKER', 'SOVEREIGNBANK', 'USBANKNA'
    #                                                       'FLAGSTARCAPITALMARKE']
    #     A = A + ['WI', 'MI', 'WA', 'IN', 'MT', 'OK', 'CA', 'KY', 'NE', 'NY', 'KS', 'IL', 'TX', 'IA'
    #                                                                                            'ND', 'OH', 'ME', 'MN',
    #              'PA', 'AL', 'FL', 'CO', 'CT', 'MD', 'AK', 'MO', 'UT', 'VA'
    #                                                                    'NJ', 'MA', 'GA', 'SC', 'NC', 'TN', 'DE', 'NH',
    #              'RI', 'OR', 'WY', 'NM', 'ID', 'WV'
    #                                            'SD', 'HI', 'LA', 'AR', 'VT', 'AZ', 'NV', 'MS', 'GU', 'PR', 'DC', 'VI']
    #     B = B + ['Other servicers', 'USBANKNA', 'CITIMORTGAGE,INC', 'BANKOFAMERICA,NA'
    #                                                                 'BACHOMELOANSERVICING', 'COUNTRYWIDE',
    #              'NATIONSTARMTGELLC'
    #              'PROVIDENTFUNDINGASSO', 'WELLSFARGOBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                           'TAYLOR,BEAN&WHITAKER', 'GMACMORTGAGE,LLC',
    #              'JPMORGANCHASEBANK,NA']
    #     C = C + ['Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE'
    #                                                                   'PROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC',
    #              'TAYLOR,BEAN&WHITAKER'
    #              'GMACMORTGAGE,LLC']
    #     A = A + ['ME', 'IL', 'NE', 'NY', 'MN', 'WA', 'CO', 'IN', 'WI', 'IA', 'AK', 'OR', 'MA', 'VA'
    #                                                                                            'KY', 'ND', 'AL', 'PA',
    #              'OH', 'MI', 'CA', 'NJ', 'SC', 'TX', 'WY', 'RI', 'TN', 'GA'
    #                                                                    'CT', 'KS', 'NC', 'DE', 'MO', 'UT', 'NH', 'OK',
    #              'MD', 'FL', 'MT', 'WV', 'HI', 'ID'
    #                                            'LA', 'VT', 'AZ', 'MS', 'AR', 'SD', 'PR', 'GU', 'NM', 'NV', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'CITIMORTGAGE,INC', 'BANKOFAMERICA,NA'
    #                                                                 'BACHOMELOANSERVICING', 'COUNTRYWIDE',
    #              'NATIONSTARMTGELLC'
    #              'PROVIDENTFUNDINGASSO', 'WELLSFARGOBANK,NA', 'BRANCHBANKING&TRUSTC'
    #                                                           'TAYLOR,BEAN&WHITAKER', 'GMACMORTGAGE,LLC',
    #              'JPMORGANCHASEBANK,NA']
    #     C = C + ['Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE'
    #                                                                   'PROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC',
    #              'TAYLOR,BEAN&WHITAKER'
    #              'GMACMORTGAGE,LLC']
    #     A = A + ['ME', 'IL', 'NE', 'NY', 'MN', 'WA', 'CO', 'IN', 'WI', 'IA', 'AK', 'OR', 'MA', 'VA'
    #                                                                                            'KY', 'ND', 'AL', 'PA',
    #              'OH', 'MI', 'CA', 'NJ', 'SC', 'TX', 'WY', 'RI', 'TN', 'GA'
    #                                                                    'CT', 'KS', 'NC', 'DE', 'MO', 'UT', 'NH', 'OK',
    #              'MD', 'FL', 'MT', 'WV', 'HI', 'ID'
    #                                            'LA', 'VT', 'AZ', 'MS', 'AR', 'SD', 'PR', 'GU', 'NM', 'NV', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'CITIMORTGAGE,INC', 'BANKOFAMERICA,NA'
    #                                                                 'COUNTRYWIDE', 'BACHOMELOANSERVICING',
    #              'PROVIDENTFUNDINGASSO'
    #              'NATIONSTARMTGELLC', 'GMACMORTGAGE,LLC', 'OCWENLOANSERVICING,L'
    #                                                       'FIFTHTHIRDBANK', 'BRANCHBANKING&TRUSTC',
    #              'JPMORGANCHASEBANK,NA'
    #              'TAYLOR,BEAN&WHITAKER']
    #     C = C + ['Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE'
    #                                                                   'PROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC',
    #              'FIRSTHORIZONHOMELOAN'
    #              'FIFTHTHIRDBANK', 'BRANCHBANKING&TRUSTC', 'WASHINGTONMUTUALBANK'
    #                                                        'TAYLOR,BEAN&WHITAKER', 'BANKOFAMERICA,NA']
    #     A = A + ['IL', 'WA', 'OH', 'WI', 'NJ', 'NY', 'MI', 'KY', 'IN', 'CO', 'GA', 'MO', 'ND', 'NC'
    #                                                                                            'CT', 'CA', 'ME', 'WV',
    #              'SC', 'MA', 'PA', 'IA', 'AK', 'NE', 'MN', 'MD', 'OR', 'NH'
    #                                                                    'WY', 'OK', 'VA', 'DE', 'UT', 'TX', 'KS', 'FL',
    #              'RI', 'AL', 'MT', 'AR', 'TN', 'VT'
    #                                            'ID', 'HI', 'AZ', 'LA', 'PR', 'NV', 'SD', 'NM', 'MS', 'GU', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                             'BACHOMELOANSERVICING', 'BANKOFAMERICA,NA', 'NATIONSTARMTGELLC'
    #                                                                                         'PROVIDENTFUNDINGASSO',
    #              'COUNTRYWIDE', 'LAKEVIEWLOANSERVICIN'
    #                             'JPMORGANCHASEBANK,NA', 'OCWENLOANSERVICING,L', 'FIFTHTHIRDBANK'
    #                                                                             'TAYLOR,BEAN&WHITAKER',
    #              'GMACMORTGAGE,LLC', 'CITIMORTGAGE,INC']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDE'
    #                                                                   'PROVIDENTFUNDINGASSO', 'FIFTHTHIRDBANK',
    #              'TAYLOR,BEAN&WHITAKER'
    #              'WASHINGTONMUTUALBANK', 'GMACMORTGAGE,LLC', 'ABNAMRO,NKACITIMORTG']
    #     A = A + ['WA', 'NJ', 'IN', 'KY', 'OR', 'IA', 'AL', 'CO', 'NY', 'MN', 'MI', 'ND', 'IL', 'AK'
    #                                                                                            'SC', 'WI', 'OK', 'NE',
    #              'ME', 'PA', 'NC', 'CT', 'OH', 'MO', 'MD', 'KS', 'VA', 'CA'
    #                                                                    'GA', 'WY', 'MA', 'LA', 'TX', 'DE', 'ID', 'MT',
    #              'FL', 'NH', 'UT', 'AR', 'SD', 'TN'
    #                                            'WV', 'NM', 'DC', 'VT', 'AZ', 'RI', 'MS', 'HI', 'NV', 'GU', 'PR']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'NATIONSTARMTGELLC'
    #                                                                     'BANKOFAMERICA,NA', 'COUNTRYWIDE',
    #              'OCWENLOANSERVICING,L'
    #              'JPMORGANCHASEBANK,NA', 'PROVIDENTFUNDINGASSO', 'CITIMORTGAGE,INC'
    #                                                              'TAYLOR,BEAN&WHITAKER', 'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDE'
    #                                                                   'FIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO',
    #              'ABNAMRO,NKACITIMORTG'
    #              'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK']
    #     A = A + ['IL', 'MN', 'NC', 'IA', 'CO', 'KY', 'NH', 'WA', 'MI', 'AK', 'PA', 'MA', 'OH', 'WI'
    #                                                                                            'NY', 'NE', 'UT', 'ND',
    #              'CA', 'CT', 'VA', 'AR', 'TX', 'ME', 'MO', 'WV', 'KS', 'OR'
    #                                                                    'IN', 'SC', 'MT', 'MD', 'WY', 'RI', 'NJ', 'OK',
    #              'FL', 'GA', 'AZ', 'TN', 'AL', 'ID'
    #                                            'VT', 'NV', 'DE', 'MS', 'LA', 'NM', 'GU', 'HI', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'NATIONSTARMTGELLC'
    #                                                                     'BANKOFAMERICA,NA', 'COUNTRYWIDE',
    #              'OCWENLOANSERVICING,L'
    #              'JPMORGANCHASEBANK,NA', 'PROVIDENTFUNDINGASSO', 'CITIMORTGAGE,INC'
    #                                                              'TAYLOR,BEAN&WHITAKER', 'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDE'
    #                                                                   'FIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO',
    #              'ABNAMRO,NKACITIMORTG'
    #              'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK']
    #     A = A + ['IL', 'MN', 'NC', 'IA', 'CO', 'KY', 'NH', 'WA', 'MI', 'AK', 'PA', 'MA', 'OH', 'WI'
    #                                                                                            'NY', 'NE', 'UT', 'ND',
    #              'CA', 'CT', 'VA', 'AR', 'TX', 'ME', 'MO', 'WV', 'KS', 'OR'
    #                                                                    'IN', 'SC', 'MT', 'MD', 'WY', 'RI', 'NJ', 'OK',
    #              'FL', 'GA', 'AZ', 'TN', 'AL', 'ID'
    #                                            'VT', 'NV', 'DE', 'MS', 'LA', 'NM', 'GU', 'HI', 'DC']
    #     B = B + ['USBANKNA', 'Other servicers', 'BRANCHBANKING&TRUSTC', 'BANKOFAMERICA,NA'
    #                                                                     'NATIONSTARMTGELLC', 'GMACMORTGAGE,LLC',
    #              'JPMORGANCHASEBANK,NA'
    #              'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'ALLYBANK']
    #     C = C + ['UCBANCNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDE'
    #                                                                   'GMACMORTGAGE,LLC', 'WASHINGTONMUTUALBANK',
    #              'TAYLOR,BEAN&WHITAKER'
    #              'FLAGSTARCAPITALMARKE', 'FIRSTHORIZONHOMELOAN']
    #     A = A + ['CT', 'OH', 'NH', 'MI', 'ND', 'WA', 'NY', 'MN', 'KY', 'CO', 'KS', 'MT', 'VA', 'IL'
    #                                                                                            'WI', 'NC', 'MD', 'ME',
    #              'RI', 'CA', 'IA', 'UT', 'FL', 'OR', 'MO', 'PA', 'IN', 'MA'
    #                                                                    'TX', 'OK', 'NE', 'NJ', 'AK', 'WY', 'HI', 'LA',
    #              'GA', 'TN', 'SC', 'AL', 'WV', 'MS'
    #                                            'VT', 'AR', 'AZ', 'PR', 'DE', 'ID', 'NM', 'GU', 'NV', 'SD', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'NATIONSTARMTGELLC', 'BANKOFAMERICA,NA'
    #                                                                  'FLAGSTARCAPITALMARKE', 'GMACMORTGAGE,LLC',
    #              'BRANCHBANKING&TRUSTC'
    #              'TAYLOR,BEAN&WHITAKER', 'WELLSFARGOBANK,NA', 'JPMORGANCHASEBANK,NA'
    #                                                           'METLIFEHOMELOANS,ADI', 'ALLYBANK']
    #     C = C + ['Other sellers', 'USBANKNA', 'COUNTRYWIDE', 'FLAGSTARCAPITALMARKE'
    #                                                          'GMACMORTGAGE,LLC', 'BRANCHBANKING&TRUSTC',
    #              'TAYLOR,BEAN&WHITAKER'
    #              'WELLSFARGOBANK,NA', 'FIRSTHORIZONHOMELOAN']
    #     A = A + ['MA', 'KS', 'NC', 'MI', 'SC', 'ND', 'IL', 'KY', 'PA', 'CO', 'NJ', 'OH', 'IA', 'NY'
    #                                                                                            'MN', 'CA', 'UT', 'OR',
    #              'IN', 'DE', 'VA', 'NH', 'WA', 'WI', 'ME', 'OK', 'CT', 'AR'
    #                                                                    'MO', 'TX', 'GA', 'AL', 'MT', 'NE', 'AK', 'ID',
    #              'TN', 'WY', 'MD', 'FL', 'VT', 'RI'
    #                                            'AZ', 'MS', 'HI', 'GU', 'LA', 'NM', 'DC', 'NV', 'WV', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'CENTRALMTGECO', 'BRANCHBANKING&TRUSTC'
    #                                                              'NATIONSTARMTGELLC', 'BANKOFAMERICA,NA',
    #              'JPMORGANCHASEBANK,NA'
    #              'FLAGSTARCAPITALMARKE', 'TAYLOR,BEAN&WHITAKER', 'ALLYBANK']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDE'
    #                                                                   'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE',
    #              'GMACMORTGAGE,LLC']
    #     A = A + ['ME', 'IL', 'WI', 'GA', 'CO', 'MO', 'IA', 'MI', 'MD', 'WY', 'KY', 'KS', 'NC', 'CT'
    #                                                                                            'WA', 'AK', 'OH', 'OR',
    #              'PA', 'NY', 'CA', 'NV', 'ND', 'TX', 'VT', 'OK', 'MN', 'FL'
    #                                                                    'UT', 'IN', 'NJ', 'MA', 'HI', 'TN', 'VA', 'NM',
    #              'ID', 'RI', 'NH', 'NE', 'SC', 'WV'
    #                                            'DC', 'AZ', 'AL', 'AR', 'VI', 'LA', 'DE', 'MS', 'MT', 'GU', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'CENTRALMTGECO', 'BRANCHBANKING&TRUSTC'
    #                                                              'NATIONSTARMTGELLC', 'BANKOFAMERICA,NA',
    #              'JPMORGANCHASEBANK,NA'
    #              'FLAGSTARCAPITALMARKE', 'TAYLOR,BEAN&WHITAKER', 'ALLYBANK']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDE'
    #                                                                   'TAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE',
    #              'GMACMORTGAGE,LLC']
    #     A = A + ['ME', 'IL', 'WI', 'GA', 'CO', 'MO', 'IA', 'MI', 'MD', 'WY', 'KY', 'KS', 'NC', 'CT'
    #                                                                                            'WA', 'AK', 'OH', 'OR',
    #              'PA', 'NY', 'CA', 'NV', 'ND', 'TX', 'VT', 'OK', 'MN', 'FL'
    #                                                                    'UT', 'IN', 'NJ', 'MA', 'HI', 'TN', 'VA', 'NM',
    #              'ID', 'RI', 'NH', 'NE', 'SC', 'WV'
    #                                            'DC', 'AZ', 'AL', 'AR', 'VI', 'LA', 'DE', 'MS', 'MT', 'GU', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                             'PROVIDENTFUNDINGASSO', 'NATIONSTARMTGELLC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSO']
    #     A = A + ['IL', 'IA', 'KY', 'WI', 'PA', 'MN', 'OH', 'NE', 'WA', 'KS', 'CA', 'NH', 'ND', 'WV'
    #                                                                                            'MI', 'AK', 'GA', 'IN',
    #              'NY', 'OR', 'MO', 'VA', 'HI', 'VT', 'CO', 'RI', 'MA', 'SC'
    #                                                                    'MT', 'NC', 'MD', 'NJ', 'FL', 'AZ', 'UT', 'ME',
    #              'TN', 'DE', 'WY', 'CT', 'AL', 'TX'
    #                                            'SD', 'MS', 'OK', 'ID', 'DC']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                             'PROVIDENTFUNDINGASSO', 'METLIFEHOMELOANS,ADI', 'WELLSFARGOBANK,NA'
    #                                                                                             'BANKOFAMERICA,NA',
    #              'PHHMTGECORP', 'JPMORGANCHASEBANK,NA']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO'
    #                                                                   'AMTRUSTBANK', 'FLAGSTARCAPITALMARKE',
    #              'WELLSFARGOBANK,NA'
    #              'BANKOFAMERICA,NA', 'METLIFEHOMELOANS,ADI', 'PHHMTGECORP']
    #     A = A + ['IL', 'AZ', 'MD', 'MI', 'ND', 'NE', 'VT', 'MO', 'IA', 'MA', 'NC', 'ME', 'KS', 'KY'
    #                                                                                            'WV', 'MN', 'NY', 'WA',
    #              'OK', 'WI', 'NJ', 'CT', 'PA', 'FL', 'CA', 'OH', 'TN', 'AK'
    #                                                                    'SD', 'RI', 'IN', 'OR', 'DC', 'DE', 'NH', 'VA',
    #              'WY', 'CO', 'SC', 'NM', 'TX', 'GA'
    #                                            'HI', 'MT', 'AL', 'UT', 'NV', 'ID', 'LA', 'AR', 'MS', 'GU']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                                     'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'METLIFEHOMELOANS,ADI', 'JPMORGANCHASEBANK,NA'
    #                                                              'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                                   'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANK'
    #                                                     'METLIFEHOMELOANS,ADI']
    #     A = A + ['CA', 'NC', 'IL', 'MN', 'OH', 'KY', 'HI', 'KS', 'MO', 'MI', 'ME', 'TN', 'WI', 'WA'
    #                                                                                            'IA', 'OR', 'VT', 'FL',
    #              'PA', 'NH', 'CO', 'MT', 'CT', 'NY', 'SC', 'AL', 'WV', 'ND'
    #                                                                    'TX', 'NE', 'OK', 'DE', 'MA', 'AK', 'MD', 'IN',
    #              'NV', 'GA', 'UT', 'NJ', 'WY', 'VA'
    #                                            'RI', 'NM', 'AZ', 'MS', 'DC', 'ID', 'AR', 'LA', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                                     'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'METLIFEHOMELOANS,ADI', 'JPMORGANCHASEBANK,NA'
    #                                                              'FIFTHTHIRDBANK']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NA'
    #                                                                   'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANK'
    #                                                     'METLIFEHOMELOANS,ADI']
    #     A = A + ['CA', 'NC', 'IL', 'MN', 'OH', 'KY', 'HI', 'KS', 'MO', 'MI', 'ME', 'TN', 'WI', 'WA'
    #                                                                                            'IA', 'OR', 'VT', 'FL',
    #              'PA', 'NH', 'CO', 'MT', 'CT', 'NY', 'SC', 'AL', 'WV', 'ND'
    #                                                                    'TX', 'NE', 'OK', 'DE', 'MA', 'AK', 'MD', 'IN',
    #              'NV', 'GA', 'UT', 'NJ', 'WY', 'VA'
    #                                            'RI', 'NM', 'AZ', 'MS', 'DC', 'ID', 'AR', 'LA', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                             'PROVIDENTFUNDINGASSO', 'METLIFEHOMELOANS,ADI', 'SUNTRUSTMORTGAGE,INC'
    #                                                                                             'BANKOFAMERICA,NA',
    #              'PHHMTGECORP', 'FREMONTBANK']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSO'
    #                                                                   'METLIFEHOMELOANS,ADI', 'SUNTRUSTMORTGAGE,INC',
    #              'BANKOFAMERICA,NA'
    #              'PHHMTGECORP', 'FREMONTBANK']
    #     A = A + ['WA', 'MO', 'NY', 'PA', 'IL', 'KS', 'WI', 'HI', 'OH', 'OK', 'MI', 'NE', 'CA', 'OR'
    #                                                                                            'MA', 'NC', 'MN', 'NH',
    #              'AZ', 'TX', 'SC', 'TN', 'ND', 'CO', 'DE', 'MD', 'KY', 'AK'
    #                                                                    'FL', 'ME', 'IA', 'IN', 'VA', 'WV', 'AL', 'CT',
    #              'GA', 'VT', 'MT', 'AR', 'UT', 'NJ'
    #                                            'NV', 'GU', 'LA', 'RI', 'WY', 'ID', 'NM', 'DC', 'MS', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'CENTRALMTGECO', 'BRANCHBANKING&TRUSTC'
    #                                                              'QUICKENLOANINC', 'PROVIDENTFUNDINGASSO',
    #              'UNIONSAVINGSBANK'
    #              'JPMORGANCHASEBANK,NA', 'FIFTHTHIRDBANK', 'PHHMTGECORP', 'BANKOFAMERICA,NA']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSO'
    #                                                                   'UNIONSAVINGSBANK', 'METLIFEHOMELOANS,ADI',
    #              'FIFTHTHIRDBANK', 'PHHMTGECORP'
    #                                'BANKOFAMERICA,NA']
    #     A = A + ['IL', 'OR', 'IA', 'MN', 'NH', 'CA', 'AZ', 'KY', 'MI', 'GA', 'WA', 'MO', 'HI', 'CO'
    #                                                                                            'NY', 'WI', 'NC', 'OH',
    #              'FL', 'CT', 'ND', 'IN', 'KS', 'SC', 'MD', 'PA', 'ME', 'WV'
    #                                                                    'VA', 'TX', 'OK', 'MA', 'NE', 'NJ', 'RI', 'VT',
    #              'AK', 'AR', 'DC', 'TN', 'WY', 'DE'
    #                                            'NV', 'UT', 'LA', 'MT', 'AL', 'NM', 'ID', 'SD']
    #     B = B + ['Other servicers', 'USBANKNA', 'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA']
    #     A = A + ['IA', 'IL', 'KY', 'OK', 'KS', 'WI', 'MO', 'FL', 'MI', 'GA', 'NC', 'CA', 'NE', 'WA'
    #                                                                                            'HI', 'MA', 'VA', 'NJ',
    #              'OH', 'SC', 'AK', 'NY', 'TX', 'ME', 'ND', 'NH', 'MD', 'CO'
    #                                                                    'OR', 'VT', 'CT', 'IN', 'MN', 'WV', 'UT', 'DE',
    #              'PA', 'SD', 'TN', 'RI', 'AL', 'AZ'
    #                                            'NM', 'WY', 'DC', 'MT']
    #     B = B + ['Other servicers', 'USBANKNA', 'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA']
    #     A = A + ['IA', 'IL', 'KY', 'OK', 'KS', 'WI', 'MO', 'FL', 'MI', 'GA', 'NC', 'CA', 'NE', 'WA'
    #                                                                                            'HI', 'MA', 'VA', 'NJ',
    #              'OH', 'SC', 'AK', 'NY', 'TX', 'ME', 'ND', 'NH', 'MD', 'CO'
    #                                                                    'OR', 'VT', 'CT', 'IN', 'MN', 'WV', 'UT', 'DE',
    #              'PA', 'SD', 'TN', 'RI', 'AL', 'AZ'
    #                                            'NM', 'WY', 'DC', 'MT']
    #     B = B + ['Other servicers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANK'
    #                                                                     'FIFTHTHIRDMTGECO', 'PROVIDENTFUNDINGASSO',
    #              'BANKOFAMERICA,NA'
    #              'METLIFEHOMELOANS,ADI', 'JPMORGANCHASEBANK,NA', 'PHHMTGECORP'
    #                                                              'SUNTRUSTMORTGAGE,INC', 'FREMONTBANK']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'FIFTHTHIRDBANK'
    #                                                                   'PROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA',
    #              'METLIFEHOMELOANS,ADI'
    #              'PHHMTGECORP', 'FREMONTBANK', 'JPMORGANCHASEBANK,NA']
    #     A = A + ['KY', 'MI', 'TX', 'IL', 'IA', 'IN', 'OR', 'CO', 'ND', 'HI', 'MO', 'OH', 'WI', 'WA'
    #                                                                                            'CA', 'ME', 'AK', 'KS',
    #              'PA', 'NY', 'OK', 'NJ', 'CT', 'WV', 'MN', 'MA', 'NH', 'FL'
    #                                                                    'NE', 'NC', 'GA', 'SC', 'RI', 'VA', 'VT', 'MT',
    #              'ID', 'AZ', 'AR', 'DE', 'MD', 'WY'
    #                                            'SD', 'NM', 'TN', 'NV', 'AL', 'UT', 'DC', 'MS', 'LA', 'GU']
    #     B = B + ['Other servicers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'UNIONSAVINGSBANK'
    #                                                                     'JPMORGANCHASEBANK,NA', 'BANKOFAMERICA,NA',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'QUICKENLOANINC', 'OCWENLOANSERVICING,L', 'ALLYBANK'
    #                                                                                'FIFTHTHIRDMTGECO',
    #              'CITIMORTGAGE,INC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'UNIONSAVINGSBANK'
    #                                                                   'METLIFEHOMELOANS,ADI', 'BANKOFAMERICA,NA',
    #              'PHHMTGECORP'
    #              'PROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC', 'FREMONTBANK', 'FIFTHTHIRDBANK'
    #                                                                         'JPMORGANCHASEBANK,NA', 'CITIMORTGAGE,INC']
    #     A = A + ['KY', 'MI', 'IL', 'MN', 'OK', 'RI', 'MD', 'MO', 'KS', 'NY', 'OR', 'SC', 'NE', 'NC'
    #                                                                                            'MA', 'FL', 'WA', 'ND',
    #              'OH', 'TX', 'IA', 'NH', 'MT', 'AK', 'CT', 'VT', 'DE', 'CA'
    #                                                                    'WV', 'IN', 'CO', 'PA', 'ME', 'WI', 'MS', 'GA',
    #              'HI', 'VA', 'NJ', 'ID', 'LA', 'SD'
    #                                            'UT', 'WY', 'AZ', 'NV', 'TN', 'NM', 'AR', 'DC', 'GU', 'AL']
    #     B = B + ['Other servicers', 'PNCBANK,NATL', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                                             'PROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA',
    #              'UNIONSAVINGSBANK'
    #              'PHHMTGECORP']
    #     C = C + ['Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNA'
    #                                                                             'PROVIDENTFUNDINGASSO',
    #              'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK'
    #                                  'PHHMTGECORP']
    #     A = A + ['IL', 'IN', 'AK', 'MO', 'OR', 'MN', 'MI', 'NC', 'NH', 'VA', 'KY', 'IA', 'WY', 'MA'
    #                                                                                            'WA', 'CA', 'ME', 'OH',
    #              'KS', 'WV', 'RI', 'OK', 'MD', 'TX', 'WI', 'NY', 'NE', 'FL'
    #                                                                    'HI', 'NJ', 'CT', 'ND', 'PA', 'SC', 'VT', 'CO',
    #              'MT', 'GA', 'TN', 'AZ', 'DE', 'MS'
    #                                            'NM', 'AL', 'UT', 'AR', 'ID', 'NV', 'LA']
    #     B = B + ['Other servicers', 'PNCBANK,NATL', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                                             'PROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA',
    #              'UNIONSAVINGSBANK'
    #              'PHHMTGECORP']
    #     C = C + ['Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNA'
    #                                                                             'PROVIDENTFUNDINGASSO',
    #              'BANKOFAMERICA,NA', 'UNIONSAVINGSBANK'
    #                                  'PHHMTGECORP']
    #     A = A + ['IL', 'IN', 'AK', 'MO', 'OR', 'MN', 'MI', 'NC', 'NH', 'VA', 'KY', 'IA', 'WY', 'MA'
    #                                                                                            'WA', 'CA', 'ME', 'OH',
    #              'KS', 'WV', 'RI', 'OK', 'MD', 'TX', 'WI', 'NY', 'NE', 'FL'
    #                                                                    'HI', 'NJ', 'CT', 'ND', 'PA', 'SC', 'VT', 'CO',
    #              'MT', 'GA', 'TN', 'AZ', 'DE', 'MS'
    #                                            'NM', 'AL', 'UT', 'AR', 'ID', 'NV', 'LA']
    #     B = B + ['Other servicers', 'USBANKNA', 'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC'
    #                                                             'PROVIDENTFUNDINGASSO']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GREENLIGHTFINANCIALS'
    #                                                                   'PROVIDENTFUNDINGASSO']
    #     A = A + ['IL', 'IA', 'ID', 'AK', 'KS', 'WA', 'VA', 'NE', 'OH', 'WY', 'NY', 'WI', 'IN', 'DE'
    #                                                                                            'HI', 'MA', 'OK', 'OR',
    #              'MN', 'CA', 'CT', 'KY', 'MI', 'MO', 'FL', 'ME', 'AZ', 'TX'
    #                                                                    'WV', 'NH', 'PA', 'ND', 'NC', 'GA', 'TN', 'MD',
    #              'VT', 'RI', 'CO', 'NV', 'MT', 'SC'
    #                                            'UT', 'AL', 'NJ', 'NM', 'AR', 'DC', 'LA']
    #     B = B + ['Other servicers', 'PNCBANK,NATL', 'USBANKNA', 'BRANCHBANKING&TRUSTC'
    #                                                             'PROVIDENTFUNDINGASSO', 'SENECAMTGESERVICING,',
    #              'BANKOFAMERICA,NA']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INC'
    #                                                                   'PROVIDENTFUNDINGASSO', 'GREENLIGHTFINANCIALS',
    #              'CALIBERFUNDINGLLC'
    #              'BANKOFAMERICA,NA']
    #     A = A + ['NE', 'VT', 'FL', 'IA', 'ND', 'KY', 'MO', 'VA', 'MN', 'IN', 'WI', 'TN', 'MA', 'AZ'
    #                                                                                            'IL', 'OR', 'WA', 'NC',
    #              'WV', 'MI', 'KS', 'CT', 'ME', 'CA', 'ID', 'NY', 'RI', 'AK'
    #                                                                    'HI', 'NH', 'MD', 'TX', 'OH', 'OK', 'GA', 'CO',
    #              'AR', 'SC', 'UT', 'MT', 'PA', 'NJ'
    #                                            'AL', 'NM', 'DC', 'WY']
    #     B = B + ['USBANKNA', 'Other servicers', 'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC'
    #                                                             'ARVESTCENTRALMTGECO', 'NATIONSTARMTGELLC',
    #              'PROVIDENTFUNDINGASSO']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO']
    #     A = A + ['CO', 'MO', 'NY', 'MD', 'OH', 'FL', 'DE', 'IA', 'VT', 'KY', 'HI', 'CA', 'KS', 'NE'
    #                                                                                            'WI', 'IL', 'NH', 'CT',
    #              'NJ', 'MN', 'VA', 'IN', 'ME', 'PA', 'OR', 'ND', 'MI', 'WV'
    #                                                                    'GA', 'MA', 'AK', 'SC', 'WA', 'OK', 'NC', 'MT',
    #              'TN', 'RI', 'AL', 'SD', 'WY', 'TX'
    #                                            'UT']
    #     B = B + ['USBANKNA', 'Other servicers', 'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC'
    #                                                             'ARVESTCENTRALMTGECO', 'NATIONSTARMTGELLC',
    #              'PROVIDENTFUNDINGASSO']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO']
    #     A = A + ['CO', 'MO', 'NY', 'MD', 'OH', 'FL', 'DE', 'IA', 'VT', 'KY', 'HI', 'CA', 'KS', 'NE'
    #                                                                                            'WI', 'IL', 'NH', 'CT',
    #              'NJ', 'MN', 'VA', 'IN', 'ME', 'PA', 'OR', 'ND', 'MI', 'WV'
    #                                                                    'GA', 'MA', 'AK', 'SC', 'WA', 'OK', 'NC', 'MT',
    #              'TN', 'RI', 'AL', 'SD', 'WY', 'TX'
    #                                            'UT']
    #     B = B + ['Other servicers', 'SUNTRUSTMORTGAGE,INC', 'NATIONSTARMTGELLC', 'USBANKNA'
    #                                                                              'PNCBANK,NATL', 'BRANCHBANKING&TRUSTC',
    #              'CALIBERHOMELOANS,INC'
    #              'NEWRESIDENTIALMTGELL', 'PHHMTGECORP', 'SENECAMTGESERVICING,']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INC'
    #                                                                   'CALIBERFUNDINGLLC', 'PHHMTGECORP']
    #     A = A + ['IA', 'CT', 'MD', 'WV', 'MN', 'AK', 'WI', 'MI', 'NC', 'NE', 'ND', 'CA', 'OK', 'KY'
    #                                                                                            'NY', 'VT', 'OH', 'NH',
    #              'ME', 'MO', 'KS', 'IL', 'VA', 'FL', 'PA', 'MA', 'IN', 'OR'
    #                                                                    'SC', 'ID', 'TX', 'CO', 'HI', 'WA', 'GA', 'TN',
    #              'UT', 'MT', 'WY', 'DC', 'AZ', 'AL'
    #                                            'AR', 'RI', 'DE', 'SD', 'NJ', 'NM', 'GU', 'NV', 'MS']
    #     B = B + ['Other servicers', 'USBANKNA', 'NATIONSTARMTGELLC', 'PNCBANK,NATL'
    #                                                                  'BRANCHBANKING&TRUSTC', 'SUNTRUSTMORTGAGE,INC',
    #              'SENECAMTGESERVICING,'
    #              'PROVIDENTFUNDINGASSO', 'CALIBERHOMELOANS,INC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'GUARANTEEDRATE,INC', 'USBANKNA'
    #                                                                             'CALIBERHOMELOANS,INC',
    #              'UNITEDSHOREFINANCIAL']
    #     A = A + ['NE', 'IL', 'IA', 'CO', 'CA', 'VA', 'MI', 'MN', 'WA', 'FL', 'KY', 'VT', 'OR', 'IN'
    #                                                                                            'PA', 'KS', 'AK', 'MO',
    #              'ME', 'WI', 'MA', 'OK', 'ND', 'TX', 'TN', 'NC', 'OH', 'GA'
    #                                                                    'HI', 'RI', 'MD', 'WV', 'SC', 'UT', 'MT', 'NJ',
    #              'CT', 'NH', 'NY', 'ID', 'AR', 'NV'
    #                                            'WY', 'SD', 'AZ', 'NM', 'DE', 'MS', 'DC', 'AL', 'LA', 'GU']
    #     B = B + ['PNCBANK,NATL', 'Other servicers', 'BRANCHBANKING&TRUSTC', 'USBANKNA'
    #                                                                         'NATIONSTARMTGELLC', 'LAKEVIEWLOANSERVICIN',
    #              'DITECHFINANCIALLLC'
    #              'SUNTRUSTMORTGAGE,INC', 'SENECAMTGESERVICING,', 'CALIBERHOMELOANS,INC'
    #                                                              'BANKOFAMERICA,NA', 'PHHMTGECORP',
    #              'PINGORALOANSERVICING', 'QUICKENLOANINC'
    #                                      'STEARNSLENDING,LLC', 'PENNYMACCORP']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INC'
    #                                                                   'CALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA',
    #              'PHHMTGECORP', 'CMGMORTGAGE,INC'
    #                             'QUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLC'
    #                                                                       'STEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS',
    #              'PENNYMACCORP']
    #     A = A + ['WI', 'IA', 'NE', 'IL', 'MI', 'PA', 'MO', 'WY', 'CA', 'OH', 'CO', 'WA', 'KY', 'IN'
    #                                                                                            'UT', 'NY', 'MN', 'KS',
    #              'ND', 'GA', 'MA', 'TN', 'NC', 'CT', 'TX', 'FL', 'OR', 'WV'
    #                                                                    'ME', 'NH', 'AZ', 'RI', 'NJ', 'VT', 'HI', 'VA',
    #              'OK', 'MT', 'SD', 'MD', 'AK', 'NV'
    #                                            'DE', 'AR', 'DC', 'SC', 'GU', 'LA', 'ID', 'NM', 'AL']
    #     B = B + ['PNCBANK,NATL', 'Other servicers', 'BRANCHBANKING&TRUSTC', 'USBANKNA'
    #                                                                         'NATIONSTARMTGELLC', 'LAKEVIEWLOANSERVICIN',
    #              'DITECHFINANCIALLLC'
    #              'SUNTRUSTMORTGAGE,INC', 'SENECAMTGESERVICING,', 'CALIBERHOMELOANS,INC'
    #                                                              'BANKOFAMERICA,NA', 'PHHMTGECORP',
    #              'PINGORALOANSERVICING', 'QUICKENLOANINC'
    #                                      'STEARNSLENDING,LLC', 'PENNYMACCORP']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INC'
    #                                                                   'CALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA',
    #              'PHHMTGECORP', 'CMGMORTGAGE,INC'
    #                             'QUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLC'
    #                                                                       'STEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS',
    #              'PENNYMACCORP']
    #     A = A + ['WI', 'IA', 'NE', 'IL', 'MI', 'PA', 'MO', 'WY', 'CA', 'OH', 'CO', 'WA', 'KY', 'IN'
    #                                                                                            'UT', 'NY', 'MN', 'KS',
    #              'ND', 'GA', 'MA', 'TN', 'NC', 'CT', 'TX', 'FL', 'OR', 'WV'
    #                                                                    'ME', 'NH', 'AZ', 'RI', 'NJ', 'VT', 'HI', 'VA',
    #              'OK', 'MT', 'SD', 'MD', 'AK', 'NV'
    #                                            'DE', 'AR', 'DC', 'SC', 'GU', 'LA', 'ID', 'NM', 'AL']
    #     B = B + ['Other servicers', 'NATIONSTARMTGELLC', 'USBANKNA', 'LAKEVIEWLOANSERVICIN'
    #                                                                  'BRANCHBANKING&TRUSTC', 'SENECAMTGESERVICING,',
    #              'STEARNSLENDING,LLC'
    #              'PINGORALOANSERVICING', 'FIFTHTHIRDMTGECO', 'SUNTRUSTMORTGAGE,INC'
    #                                                          'ROUNDPOINTMTGESERVIC', 'BANKOFAMERICA,NA',
    #              'CALIBERHOMELOANS,INC'
    #              'QUICKENLOANINC', 'FRANKLINAMERICANMTGE']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INC'
    #                                                                   'PHHMTGECORP', 'FIFTHTHIRDBANK',
    #              'SUNTRUSTMORTGAGE,INC'
    #              'UNITEDSHOREFINANCIAL', 'BANKOFAMERICA,NA', 'CALIBERHOMELOANS,INC'
    #                                                          'STEARNSLENDING,INC', 'FLAGSTARBANK,FSB',
    #              'LOANDEPOTCOM,LLC'
    #              'FRANKLINAMERICANMTGE']
    #     A = A + ['IL', 'VA', 'MO', 'FL', 'MA', 'IA', 'NE', 'MI', 'KY', 'TX', 'ME', 'MN', 'IN', 'TN'
    #                                                                                            'OH', 'AK', 'WI', 'KS',
    #              'NC', 'CO', 'PA', 'MD', 'CT', 'GA', 'CA', 'WV', 'NY', 'VT'
    #                                                                    'OR', 'ID', 'NV', 'WA', 'UT', 'SC', 'WY', 'NH',
    #              'ND', 'RI', 'HI', 'OK', 'AZ', 'SD'
    #                                            'LA', 'NJ', 'DE', 'AL', 'MS', 'NM', 'AR', 'DC']
    #     B = B + ['Other servicers', 'NATIONSTARMTGELLC', 'USBANKNA', 'LAKEVIEWLOANSERVICIN'
    #                                                                  'BRANCHBANKING&TRUSTC', 'ROUNDPOINTMTGESERVIC',
    #              'SENECAMTGESERVICING,'
    #              'CALIBERHOMELOANS,INC', 'PINGORALOANSERVICING', 'QUICKENLOANINC'
    #                                                              'STEARNSLENDING,LLC', 'PNCBANK,NATL',
    #              'FRANKLINAMERICANMTGE'
    #              'BANKOFAMERICA,NA']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STONEGATEMTGECORP'
    #                                                                   'STEARNSLENDING,LLC', 'LOANDEPOTCOM,LLC',
    #              'CALIBERHOMELOANS,INC'
    #              'GUARANTEEDRATE,INC', 'QUICKENLOANINC', 'PHHMTGECORP'
    #                                                      'FRANKLINAMERICANMTGE', 'BANKOFAMERICA,NA']
    #     A = A + ['FL', 'KS', 'KY', 'NY', 'MD', 'MN', 'CO', 'NE', 'IA', 'OH', 'IL', 'AZ', 'MO', 'MA'
    #                                                                                            'MI', 'NC', 'ND', 'IN',
    #              'RI', 'PA', 'UT', 'ME', 'ID', 'WI', 'NV', 'CT', 'OK', 'NH'
    #                                                                    'VT', 'WA', 'DC', 'OR', 'HI', 'DE', 'TX', 'TN',
    #              'CA', 'SC', 'GA', 'VA', 'MT', 'NJ'
    #                                            'AK', 'WV', 'AL', 'AR', 'NM', 'WY', 'LA']
    #     B = B + ['Other servicers', 'NATIONSTARMTGELLC', 'BRANCHBANKING&TRUSTC'
    #                                                      'LAKEVIEWLOANSERVICIN', 'USBANKNA', 'PROVIDENTFUNDINGASSO'
    #                                                                                          'ROUNDPOINTMTGESERVIC',
    #              'CALIBERHOMELOANS,INC', 'PINGORALOANSERVICING'
    #                                      'SUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,IN'
    #                                                       'GUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC',
    #              'LOANDEPOTCOM,LLC'
    #              'SUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLC'
    #                                                        'FLAGSTARBANK,FSB']
    #     A = A + ['WI', 'CO', 'MN', 'MO', 'IA', 'NC', 'NE', 'KS', 'HI', 'ND', 'IL', 'MI', 'IN', 'AL'
    #                                                                                            'KY', 'GA', 'OK', 'MA',
    #              'ME', 'WA', 'UT', 'AZ', 'NY', 'SC', 'NJ', 'FL', 'PA', 'VT'
    #                                                                    'OR', 'TX', 'NH', 'RI', 'NV', 'OH', 'TN', 'CA',
    #              'ID', 'MT', 'AK', 'CT', 'NM', 'LA'
    #                                            'MD', 'DC', 'VA', 'AR']
    #     B = B + ['Other servicers', 'NATIONSTARMTGELLC', 'BRANCHBANKING&TRUSTC'
    #                                                      'LAKEVIEWLOANSERVICIN', 'USBANKNA', 'PROVIDENTFUNDINGASSO'
    #                                                                                          'ROUNDPOINTMTGESERVIC',
    #              'CALIBERHOMELOANS,INC', 'PINGORALOANSERVICING'
    #                                      'SUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,IN'
    #                                                       'GUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC',
    #              'LOANDEPOTCOM,LLC'
    #              'SUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLC'
    #                                                        'FLAGSTARBANK,FSB']
    #     A = A + ['WI', 'CO', 'MN', 'MO', 'IA', 'NC', 'NE', 'KS', 'HI', 'ND', 'IL', 'MI', 'IN', 'AL'
    #                                                                                            'KY', 'GA', 'OK', 'MA',
    #              'ME', 'WA', 'UT', 'AZ', 'NY', 'SC', 'NJ', 'FL', 'PA', 'VT'
    #                                                                    'OR', 'TX', 'NH', 'RI', 'NV', 'OH', 'TN', 'CA',
    #              'ID', 'MT', 'AK', 'CT', 'NM', 'LA'
    #                                            'MD', 'DC', 'VA', 'AR']
    #     B = B + ['Other servicers', 'NATIONSTARMTGELLC', 'USBANKNA', 'ARVESTCENTRALMTGECO'
    #                                                                  'LAKEVIEWLOANSERVICIN', 'BRANCHBANKING&TRUSTC']
    #     C = C + ['Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC']
    #     A = A + ['NY', 'MO', 'IL', 'TX', 'GA', 'MN', 'ME', 'NE', 'IA', 'NC', 'NV', 'MI', 'CA', 'ID'
    #                                                                                            'VT', 'MA', 'OH', 'PA',
    #              'KS', 'IN', 'WI', 'ND', 'NH', 'SD', 'KY', 'MD', 'SC', 'UT'
    #                                                                    'HI', 'CO', 'WA', 'MT', 'OR', 'VA', 'FL', 'CT',
    #              'OK', 'TN', 'DE', 'WY']
    #     B = B + ['Other servicers', 'LAKEVIEWLOANSERVICIN', 'BRANCHBANKING&TRUSTC'
    #                                                         'USBANKNA', 'ARVESTCENTRALMTGECO', 'PNCBANK,NATL',
    #              'SENECAMTGESERVICING,'
    #              'PINGORALOANSERVICING']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STEARNSLENDING,LLC']
    #     A = A + ['NC', 'NE', 'IL', 'MI', 'KY', 'MO', 'OR', 'GA', 'ME', 'TX', 'ID', 'PA', 'KS', 'CA'
    #                                                                                            'UT', 'ND', 'SC', 'IN',
    #              'IA', 'RI', 'VT', 'NY', 'OK', 'VA', 'FL', 'MA', 'WA', 'WV'
    #                                                                    'MT', 'OH', 'DC', 'CO', 'HI', 'MN', 'WI', 'TN',
    #              'WY', 'CT', 'NH', 'MD', 'AZ']
    #     B = B + ['Other servicers', 'ARVESTCENTRALMTGECO', 'PNCBANK,NATL', 'USBANKNA'
    #                                                                        'LAKEVIEWLOANSERVICIN', 'DITECHFINANCIALLLC',
    #              'BRANCHBANKING&TRUSTC'
    #              'MATRIXFINANCIALSERVI', 'SUNTRUSTMORTGAGE,INC', 'PINGORALOANSERVICING']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC']
    #     A = A + ['MI', 'IL', 'OR', 'OH', 'MN', 'ME', 'ND', 'GA', 'CA', 'UT', 'SC', 'NC', 'TX', 'NE'
    #                                                                                            'PA', 'MA', 'MO', 'DE',
    #              'KY', 'IA', 'WV', 'IN', 'AK', 'VT', 'CO', 'KS', 'FL', 'AR'
    #                                                                    'ID', 'NH', 'WI', 'TN', 'WY', 'AL', 'MT', 'OK',
    #              'CT', 'AZ', 'NY', 'WA', 'HI', 'VA']
    #     B = B + ['Other servicers', 'ARVESTCENTRALMTGECO', 'PNCBANK,NATL', 'USBANKNA'
    #                                                                        'LAKEVIEWLOANSERVICIN', 'DITECHFINANCIALLLC',
    #              'BRANCHBANKING&TRUSTC'
    #              'MATRIXFINANCIALSERVI', 'SUNTRUSTMORTGAGE,INC', 'PINGORALOANSERVICING']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC']
    #     A = A + ['MI', 'IL', 'OR', 'OH', 'MN', 'ME', 'ND', 'GA', 'CA', 'UT', 'SC', 'NC', 'TX', 'NE'
    #                                                                                            'PA', 'MA', 'MO', 'DE',
    #              'KY', 'IA', 'WV', 'IN', 'AK', 'VT', 'CO', 'KS', 'FL', 'AR'
    #                                                                    'ID', 'NH', 'WI', 'TN', 'WY', 'AL', 'MT', 'OK',
    #              'CT', 'AZ', 'NY', 'WA', 'HI', 'VA']
    #     B = B + ['Other servicers', 'ARVESTCENTRALMTGECO', 'PNCBANK,NATL', 'USBANKNA'
    #                                                                        'BRANCHBANKING&TRUSTC']
    #     C = C + ['Other sellers', 'BRANCHBANKING&TRUSTC']
    #     A = A + ['OR', 'MO', 'IL', 'NH', 'IN', 'WI', 'KS', 'MI', 'MN', 'AK', 'KY', 'DE', 'HI', 'CO'
    #                                                                                            'OH', 'SC', 'IA', 'WA',
    #              'NY', 'CA', 'VT', 'GA', 'ID', 'FL', 'MT', 'MA']
    #
    #     a = set(A)
    #     b = set(B)
    #     c = set(C)
    #
    #     print C
    #
    #
    #     A = ['NYAL', 'WA', 'CONY', 'WI', 'DENV', 'WV', 'LACT', 'ORMA', 'KSUT', 'WY', 'MAWA', 'MEOR', 'ARID', 'KYWV', 'IDHI', 'DEHI', 'UTWY', 'RI', 'WVSD', 'CAWV', 'GU', 'NVAR', 'CAUT', 'GAHI', 'GA', 'AZMN', 'OK', 'OH', 'TXSD', 'IDNC', 'SDUT', 'MENE', 'FLHI', 'OR', 'IAND', 'WAHI', 'TNKY', 'NJNV', 'NVDE', 'AKFL', 'HI', 'WYSD', 'IANY', 'PR', 'SCUT', 'MDOR', 'VTNE', 'ALND', 'GACT', 'TNID', 'PA', 'MICA', 'NJFL', 'IDDE', 'NJTX', 'COOR', 'NEKS', 'INPA', 'NEKY', 'SCKS', 'NEPA', 'AKLA', 'CAGA', 'VANJ', 'IAIN', 'ME', 'VTID', 'TXKS', 'WINY', 'MA', 'UT', 'MO', 'MN', 'MI', 'MTTN', 'MATX', 'MT', 'SDLA', 'MS', 'KYOH', 'SCMT', 'MSNM', 'FLNE', 'WINE', 'PAOR', 'COSD', 'ALAK', 'NHWY', 'ALAR', 'ORIN', 'MNNC', 'NCUT', 'VAKY', 'FL', 'INMO', 'NH', 'MAMI', 'NJ', 'AZ', 'NM', 'ARMO', 'NC', 'ND', 'NE', 'ID', 'WVDC', 'NY', 'NCMT', 'NVWY', 'IDLA', 'TXUT', 'FLUT', 'NV', 'NHVT', 'CO', 'CTWA', 'MD', 'CA', 'WVMT', 'MSVT', 'ORSC', 'WAPA', 'OKCO', 'MOIN', 'WVME', 'CT', 'UTNM', 'INUT', 'KS', 'VTOR', 'NYMN', 'NYMO', 'SC', 'MDNH', 'KY', 'AKHI', 'SD', 'NEWI', 'AZNM', 'TNOH', 'WVVA', 'DE', 'DC', 'TNTX', 'VARI', 'PRSD', 'AKSD', 'TXWV', 'TX', 'LA', 'NEFL', 'ARRI', 'KYNY', 'TN', 'IDVT', 'ORKS', 'NCMA', 'NCCT', 'WAIA', 'LAUT', 'CAMD', 'VA', 'AZIL', 'NDTX', 'NCTN', 'VI', 'AK', 'AL', 'TNWV', 'AR', 'VT', 'IL', 'UTHI', 'IN', 'IA', 'NEGA', 'INTX', 'MTAR', 'RIAR', 'AKSC', 'LAMD', 'WVMI', 'WACA', 'RIAZ', 'NJAL', 'NJAK', 'ALKY', 'COOH', 'NMHI', 'ILWI', 'WVGA']
    #     B = ['ALLYBANK', 'OCWENLOANSERVICING,LFIFTHTHIRDBANK', 'OLDKENTMTGECOCHASEMTGECO', 'DITECHFINANCIALLLCSUNTRUSTMORTGAGE,INC', 'HOMESIDELENDING,INCBAMORTGAGE,LLC', 'PNCBANK,NATLBRANCHBANKING&TRUSTC', 'USBANKNALAKEVIEWLOANSERVICIN', 'CHASEMTGECOGMACMTGECORP', 'BRANCHBANKING&TRUSTCMATRIXFINANCIALSERVI', 'PINGORALOANSERVICING', 'WASHINGTONMUTUALBANKSUNTRUSTMORTGAGE,INC', 'BRANCHBANKING&TRUSTCNATIONSTARMTGELLC', 'WELLSFARGOBANK,NATAYLOR,BEAN&WHITAKER', 'OCWENLOANSERVICING,LJPMORGANCHASEBANK,NA', 'BRANCHBANKING&TRUSTCBACHOMELOANSERVICING', 'JPMORGANCHASEBANK,NAMETLIFEHOMELOANS,ADI', 'USBANKNA', 'TAYLOR,BEAN&WHITAKER', 'BRANCHBANKING&TRUSTCFTMTGESERVICES,INC', 'BRANCHBANKING&TRUSTCQUICKENLOANINC', 'NATIONSTARMTGELLCPROVIDENTFUNDINGASSO', 'JPMORGANCHASEBANK,NATAYLOR,BEAN&WHITAKER', 'BRANCHBANKING&TRUSTCUSBANKNA', 'CHASEHOMEFINANCELLC', 'BANKOFAMERICA,NAJPMORGANCHASEBANK,NA', 'COUNTRYWIDEBANKOFAMERICA,NA', 'USBANKNABRANCHBANKING&TRUSTC', 'CITIMORTGAGE,INCBANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGACHASEMANHATTANMTGECO', 'WELLSFARGOHOMEMORTGA', 'PHHMTGECORP', 'WELLSFARGOBANK,NA', 'COUNTRYWIDEBRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSONATIONSTARMTGELLC', 'ARVESTCENTRALMTGECOLAKEVIEWLOANSERVICIN', 'USBANKNANATIONSTARMTGELLC', 'SENECAMTGESERVICING,', 'NATIONSTARMTGELLCBANKOFAMERICA,NA', 'JPMORGANCHASEBANK,NAFLAGSTARCAPITALMARKE', 'PRINCIPALRESIDENTIAL', 'HOMESIDELENDING,INC', 'TAYLOR,BEAN&WHITAKERWASHINGTONMUTUALBANK', 'NATIONSTARMTGELLC', 'WELLSFARGOBANK,NABRANCHBANKING&TRUSTC', 'WASHINGTONMUTUALBANK', 'PNCMTGESERVICES,INCCHASEHOMEFINANCELLC', 'PRINCIPALRESIDENTIALBANKOFAMERICA,NA', 'BRANCHBANKING&TRUSTCTAYLOR,BEAN&WHITAKER', 'QUICKENLOANINCSTEARNSLENDING,LLC', 'FIFTHTHIRDBANKGMACMTGECORP', 'FIFTHTHIRDBANKWELLSFARGOBANK,NA', 'STEARNSLENDING,LLCPINGORALOANSERVICING', 'BRANCHBANKING&TRUSTCPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTCWELLSFARGOBANK,NA', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'LAKEVIEWLOANSERVICIN', 'SUNTRUSTMORTGAGE,INCBANKOFAMERICA,NA', 'FIFTHTHIRDBANKBRANCHBANKING&TRUSTC', 'COUNTRYWIDECHASEHOMEFINANCELLC', 'NATLCITYMTGECOCHASEMTGECO', 'SENECAMTGESERVICING,PINGORALOANSERVICING', 'JPMORGANCHASEBANK,NANATLCITYMTGECO', 'BRANCHBANKING&TRUSTCWASHINGTONMUTUALBANK', 'JPMORGANCHASEBANK,NAFIFTHTHIRDBANK', 'FRANKLINAMERICANMTGE', 'WELLSFARGOBANK,NAFIFTHTHIRDBANK', 'QUICKENLOANINC', 'USBANKNANATLCITYMTGECO', 'BANKOFAMERICA,NANATIONSTARMTGELLC', 'PENNYMACCORP', 'LAKEVIEWLOANSERVICINBRANCHBANKING&TRUSTC', 'PNCMTGESERVICES,INCNATIONSTARMTGELLC', 'NATIONSTARMTGELLCBACHOMELOANSERVICING', 'BRANCHBANKING&TRUSTCARVESTCENTRALMTGECO', 'BANKOFAMERICA,NACOUNTRYWIDE', 'BANKOFAMERICA,NABACHOMELOANSERVICING', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'FIFTHTHIRDMTGECO', 'Other servicers', 'BANKOFAMERICA,NAHOMESIDELENDING,INC', 'CENDANTMTGECORPORATIABNAMROMTGEGROUP,INC', 'BACHOMELOANSERVICINGNATIONSTARMTGELLC', 'DITECHFINANCIALLLC', 'PINGORALOANSERVICINGSUNTRUSTMORTGAGE,INC', 'PRINCIPALRESIDENTIALBRANCHBANKING&TRUSTC', 'CALIBERHOMELOANS,INCBANKOFAMERICA,NA', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'BANKOFAMERICA,NABAMORTGAGE,LLC', 'ARVESTCENTRALMTGECO', 'WELLSFARGOBANK,NAABNAMROMTGEGROUP,INC', 'GMACMTGECORPWELLSFARGOHOMEMORTGA', 'SUNTRUSTMORTGAGE,INC', 'BANKOFAMERICA,NA', 'ABNAMROMTGEGROUP,INC', 'PNCMTGESERVICES,INC', 'NATLCITYMTGECOBRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANKTAYLOR,BEAN&WHITAKER', 'CHASEHOMEFINANCELLCCITIMORTGAGE,INC', 'WASHINGTONMUTUALHOME', 'JPMORGANCHASEBANK,NA', 'FIFTHTHIRDBANK', 'ROUNDPOINTMTGESERVIC', 'BANKOFAMERICA,NAMETLIFEHOMELOANS,ADI', 'PNCMTGESERVICES,INCCITIMORTGAGE,INC', 'BRANCHBANKING&TRUSTCLAKEVIEWLOANSERVICIN', 'ALLYBANKFIFTHTHIRDMTGECO', 'WELLSFARGOBANK,NACITIMORTGAGE,INC', 'FIFTHTHIRDBANKFIFTHTHIRDMTGECO', 'UNIONSAVINGSBANKPHHMTGECORP', 'OLDKENTMTGECO', 'CHASEMANHATTANMTGECO', 'STEARNSLENDING,LLC', 'SENECAMTGESERVICING,PROVIDENTFUNDINGASSO', 'CALIBERHOMELOANS,INCNEWRESIDENTIALMTGELL', 'CALIBERHOMELOANS,INC', 'BACHOMELOANSERVICING', 'PHHMTGECORPSUNTRUSTMORTGAGE,INC', 'SUNTRUSTMORTGAGE,INCROUNDPOINTMTGESERVIC', 'COUNTRYWIDE', 'FTMTGESERVICES,INCWASHINGTONMUTUALBANK', 'BANKOFAMERICA,NAFLAGSTARCAPITALMARKE', 'GMACMTGECORP', 'CITIMORTGAGE,INCNATIONSTARMTGELLC', 'CHASEHOMEFINANCELLCJPMORGANCHASEBANK,NA', 'FREMONTBANK', 'PNCBANK,NATL', 'CITIMORTGAGE,INC', 'NATLCITYMTGECO', 'OCWENLOANSERVICING,L', 'FTMTGESERVICES,INC', 'CITIMORTGAGE,INCTAYLOR,BEAN&WHITAKER', 'PRINCIPALRESIDENTIALWASHINGTONMUTUALBANK', 'METLIFEHOMELOANS,ADI', 'PROVIDENTFUNDINGASSO', 'FRANKLINAMERICANMTGEBANKOFAMERICA,NA', 'CENDANTMTGECORPORATICOUNTRYWIDE', 'CHASEMTGECO', 'BRANCHBANKING&TRUSTC', 'CENTRALMTGECO', 'PNCMTGESERVICES,INCUSBANKNA', 'CALIBERHOMELOANS,INCQUICKENLOANINC', 'NATIONSTARMTGELLCOCWENLOANSERVICING,L', 'FLAGSTARCAPITALMARKE', 'PNCBANK,NATLPNCMTGESERVICES,INC', 'COUNTRYWIDEWELLSFARGOBANK,NA', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'BRANCHBANKING&TRUSTCFIFTHTHIRDBANK', 'PROVIDENTFUNDINGASSOROUNDPOINTMTGESERVIC', 'LAKEVIEWLOANSERVICINJPMORGANCHASEBANK,NA', 'NATLCITYMTGECOPNCMTGESERVICES,INC', 'GMACMTGECORPCHASEMANHATTANMTGECO', 'CITIMORTGAGE,INCBACHOMELOANSERVICING', 'CITIMORTGAGE,INCBRANCHBANKING&TRUSTC', 'UNIONSAVINGSBANK', 'SENECAMTGESERVICING,CALIBERHOMELOANS,INC', 'UNIONSAVINGSBANKJPMORGANCHASEBANK,NA', 'PROVIDENTFUNDINGASSOABNAMROMTGEGROUP,INC', 'WELLSFARGOBANK,NACOUNTRYWIDE', 'USBANKNAPNCBANK,NATL', 'PNCBANK,NATLABNAMROMTGEGROUP,INC', 'GMACMORTGAGE,LLC', 'ABNAMROMTGEGROUP,INCCENDANTMTGECORPORATI']
    #     C = ['Other sellers', 'FT MORTGAGE COMPANIE', 'OLD KENT MORTGAGE CONATIONAL CITY MORTGA', 'FIRST UNION CAPITAL', 'FLEET MORTGAGE CORPOCROSSLAND MORTGAGE C', 'GMAC MORTGAGE CORPOR', 'ACCUBANC MORTGAGE CONORWEST MORTGAGE, IN', 'FLAGSTAR BANK, FSB', 'NATIONSBANC MORTGAGEHOMESIDE LENDING, IN', 'RESOURCE BANCSHARES', 'PRINCIPAL RESIDENTIACHASE MANHATTAN MORT', 'NAMCO ASSET MANAGEME', 'BANKAMERICA MORTGAGEPNC MORTGAGE CORPORA', 'G N MORTGAGE CORPORA', "WASHINGTON MUTUAL BASTANDARD FEDERAL BANBISHOP'S GATE RESIDENATIONSBANK, N.A.COUNTRYWIDE HOME LOA", 'Other sellers', 'NATIONAL CITY MORTGA', 'OLD KENT MORTGAGE COCROSSLAND MORTGAGE C', 'CHASE MANHATTAN MORT', 'FT MORTGAGE COMPANIEACCUBANC MORTGAGE CO', 'NORWEST MORTGAGE, IN', 'G N MORTGAGE CORPORABANK OF AMERICA, N.A', 'NATIONSBANC MORTGAGE', "FLAGSTAR BANK, FSBPRINCIPAL RESIDENTIABISHOP'S GATE RESIDEGE CAPITAL MORTGAGEFIRSTAR BANK, N.A.", 'PNC MORTGAGE CORPORA', 'ABN AMRO MORTGAGE GRCOUNTRYWIDE HOME LOA', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC', 'BANKOFAMERICA,NAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIALBISHOPSGATERESIDENTI', 'FTMTGECOMPANIES', 'GECAPITALMTGESERVICEFIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC', 'BANKOFAMERICA,NAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIALBISHOPSGATERESIDENTI', 'FTMTGECOMPANIES', 'GECAPITALMTGESERVICEFIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCBISHOPSGATERESIDENTI', 'PRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOANPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEFIFTHTHIRDBANK', 'Other sellers', 'NATLCITYMTGECO', 'OLDKENTMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'CROSSLANDMTGECORPPRINCIPALRESIDENTIAL', 'BISHOPSGATERESIDENTI', 'PNCMTGECORPOFAMERICAFIRSTARBANK,NA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCPRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN', 'BISHOPSGATERESIDENTIPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCPRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN', 'BISHOPSGATERESIDENTIPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'PROVIDENTFUNDINGASSO', 'TAYLOR,BEAN&WHITAKERABNAMROMTGEGROUP,INC', 'PRINCIPALRESIDENTIAL', 'WELLSFARGOHOMEMORTGAFLAGSTARBANK,FSB', 'SUNTRUSTMORTGAGE,INC', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA', 'USBANKNA', 'Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA', 'USBANKNA', 'WELLSFARGOBANK', 'Other sellers', 'TAYLOR,BEAN&WHITAKERFIFTHTHIRDBANK', 'Other sellers', 'TAYLOR,BEAN&WHITAKER', 'CHASEMANHATTANMTGECOBRANCHBANKING&TRUSTC', 'Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA', 'Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA', 'Other sellers', 'GMACMTGECORP', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKERPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'CHASEHOMEFINANCELLCUSBANKNA', 'FIFTHTHIRDBANK', 'ABNAMROMTGEGROUP,INC', 'WELLSFARGOCANKCNA', 'Other sellers', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKERABNAMROMTGEGROUP,INC', 'USBANKNA', 'FLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORPTAYLOR,BEAN&WHITAKER', 'USBANKNA', 'WASHINGTONMUTUALBANKFLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORPTAYLOR,BEAN&WHITAKER', 'USBANKNA', 'WASHINGTONMUTUALBANKFLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'USBANKNABRANCHBANKING&TRUSTC', 'SOVEREIGNBANK', 'FIFTHTHIRDBANKWELLSFARGOBANK,NA', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKERCHASEHOMEFINANCELLC', 'Other sellers', 'COUNTRYWIDE', 'ABNAMROMTGEGROUP,INCPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANKGMACMTGECORP', 'TAYLOR,BEAN&WHITAKER', 'SOVEREIGNBANK', 'USBANKNAFLAGSTARCAPITALMARKE', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERGMACMORTGAGE,LLC', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERGMACMORTGAGE,LLC', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC', 'FIRSTHORIZONHOMELOANFIFTHTHIRDBANK', 'BRANCHBANKING&TRUSTC', 'WASHINGTONMUTUALBANKTAYLOR,BEAN&WHITAKER', 'BANKOFAMERICA,NA', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'FIFTHTHIRDBANK', 'TAYLOR,BEAN&WHITAKERWASHINGTONMUTUALBANK', 'GMACMORTGAGE,LLC', 'ABNAMRO,NKACITIMORTG', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEFIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO', 'ABNAMRO,NKACITIMORTGTAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEFIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO', 'ABNAMRO,NKACITIMORTGTAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK', 'UCBANCNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEGMACMORTGAGE,LLC', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKERFLAGSTARCAPITALMARKE', 'FIRSTHORIZONHOMELOAN', 'Other sellers', 'USBANKNA', 'COUNTRYWIDE', 'FLAGSTARCAPITALMARKEGMACMORTGAGE,LLC', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERWELLSFARGOBANK,NA', 'FIRSTHORIZONHOMELOAN', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDETAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'GMACMORTGAGE,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDETAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'GMACMORTGAGE,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSOAMTRUSTBANK', 'FLAGSTARCAPITALMARKE', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'METLIFEHOMELOANS,ADI', 'PHHMTGECORP', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'UNIONSAVINGSBANK', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANKMETLIFEHOMELOANS,ADI', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'UNIONSAVINGSBANK', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANKMETLIFEHOMELOANS,ADI', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSOMETLIFEHOMELOANS,ADI', 'SUNTRUSTMORTGAGE,INC', 'BANKOFAMERICA,NAPHHMTGECORP', 'FREMONTBANK', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSOUNIONSAVINGSBANK', 'METLIFEHOMELOANS,ADI', 'FIFTHTHIRDBANK', 'PHHMTGECORPBANKOFAMERICA,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'FIFTHTHIRDBANKPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'METLIFEHOMELOANS,ADIPHHMTGECORP', 'FREMONTBANK', 'JPMORGANCHASEBANK,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'UNIONSAVINGSBANKMETLIFEHOMELOANS,ADI', 'BANKOFAMERICA,NA', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC', 'FREMONTBANK', 'FIFTHTHIRDBANKJPMORGANCHASEBANK,NA', 'CITIMORTGAGE,INC', 'Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNAPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'UNIONSAVINGSBANKPHHMTGECORP', 'Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNAPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'UNIONSAVINGSBANKPHHMTGECORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GREENLIGHTFINANCIALSPROVIDENTFUNDINGASSO', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCPROVIDENTFUNDINGASSO', 'GREENLIGHTFINANCIALS', 'CALIBERFUNDINGLLCBANKOFAMERICA,NA', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERFUNDINGLLC', 'PHHMTGECORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'GUARANTEEDRATE,INC', 'USBANKNACALIBERHOMELOANS,INC', 'UNITEDSHOREFINANCIAL', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA', 'PHHMTGECORP', 'CMGMORTGAGE,INCQUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLCSTEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS', 'PENNYMACCORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA', 'PHHMTGECORP', 'CMGMORTGAGE,INCQUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLCSTEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS', 'PENNYMACCORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCPHHMTGECORP', 'FIFTHTHIRDBANK', 'SUNTRUSTMORTGAGE,INCUNITEDSHOREFINANCIAL', 'BANKOFAMERICA,NA', 'CALIBERHOMELOANS,INCSTEARNSLENDING,INC', 'FLAGSTARBANK,FSB', 'LOANDEPOTCOM,LLCFRANKLINAMERICANMTGE', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STONEGATEMTGECORPSTEARNSLENDING,LLC', 'LOANDEPOTCOM,LLC', 'CALIBERHOMELOANS,INCGUARANTEEDRATE,INC', 'QUICKENLOANINC', 'PHHMTGECORPFRANKLINAMERICANMTGE', 'BANKOFAMERICA,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,INGUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC', 'LOANDEPOTCOM,LLCSUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLCFLAGSTARBANK,FSB', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,INGUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC', 'LOANDEPOTCOM,LLCSUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLCFLAGSTARBANK,FSB', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STEARNSLENDING,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC']

if __name__ == "__main__":
    Playground()





# 'servicer_name': ['ALLYBANK', 'OCWENLOANSERVICING,LFIFTHTHIRDBANK', 'OLDKENTMTGECOCHASEMTGECO', 'DITECHFINANCIALLLCSUNTRUSTMORTGAGE,INC', 'HOMESIDELENDING,INCBAMORTGAGE,LLC', 'PNCBANK,NATLBRANCHBANKING&TRUSTC', 'USBANKNALAKEVIEWLOANSERVICIN', 'CHASEMTGECOGMACMTGECORP', 'BRANCHBANKING&TRUSTCMATRIXFINANCIALSERVI', 'PINGORALOANSERVICING', 'WASHINGTONMUTUALBANKSUNTRUSTMORTGAGE,INC', 'BRANCHBANKING&TRUSTCNATIONSTARMTGELLC', 'WELLSFARGOBANK,NATAYLOR,BEAN&WHITAKER', 'OCWENLOANSERVICING,LJPMORGANCHASEBANK,NA', 'BRANCHBANKING&TRUSTCBACHOMELOANSERVICING', 'JPMORGANCHASEBANK,NAMETLIFEHOMELOANS,ADI', 'USBANKNA', 'TAYLOR,BEAN&WHITAKER', 'BRANCHBANKING&TRUSTCFTMTGESERVICES,INC', 'BRANCHBANKING&TRUSTCQUICKENLOANINC', 'NATIONSTARMTGELLCPROVIDENTFUNDINGASSO', 'JPMORGANCHASEBANK,NATAYLOR,BEAN&WHITAKER', 'BRANCHBANKING&TRUSTCUSBANKNA', 'CHASEHOMEFINANCELLC', 'BANKOFAMERICA,NAJPMORGANCHASEBANK,NA', 'COUNTRYWIDEBANKOFAMERICA,NA', 'USBANKNABRANCHBANKING&TRUSTC', 'CITIMORTGAGE,INCBANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGACHASEMANHATTANMTGECO', 'WELLSFARGOHOMEMORTGA', 'PHHMTGECORP', 'WELLSFARGOBANK,NA', 'COUNTRYWIDEBRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSONATIONSTARMTGELLC', 'ARVESTCENTRALMTGECOLAKEVIEWLOANSERVICIN', 'USBANKNANATIONSTARMTGELLC', 'SENECAMTGESERVICING,', 'NATIONSTARMTGELLCBANKOFAMERICA,NA', 'JPMORGANCHASEBANK,NAFLAGSTARCAPITALMARKE', 'PRINCIPALRESIDENTIAL', 'HOMESIDELENDING,INC', 'TAYLOR,BEAN&WHITAKERWASHINGTONMUTUALBANK', 'NATIONSTARMTGELLC', 'WELLSFARGOBANK,NABRANCHBANKING&TRUSTC', 'WASHINGTONMUTUALBANK', 'PNCMTGESERVICES,INCCHASEHOMEFINANCELLC', 'PRINCIPALRESIDENTIALBANKOFAMERICA,NA', 'BRANCHBANKING&TRUSTCTAYLOR,BEAN&WHITAKER', 'QUICKENLOANINCSTEARNSLENDING,LLC', 'FIFTHTHIRDBANKGMACMTGECORP', 'FIFTHTHIRDBANKWELLSFARGOBANK,NA', 'STEARNSLENDING,LLCPINGORALOANSERVICING', 'BRANCHBANKING&TRUSTCPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTCWELLSFARGOBANK,NA', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'LAKEVIEWLOANSERVICIN', 'SUNTRUSTMORTGAGE,INCBANKOFAMERICA,NA', 'FIFTHTHIRDBANKBRANCHBANKING&TRUSTC', 'COUNTRYWIDECHASEHOMEFINANCELLC', 'NATLCITYMTGECOCHASEMTGECO', 'SENECAMTGESERVICING,PINGORALOANSERVICING', 'JPMORGANCHASEBANK,NANATLCITYMTGECO', 'BRANCHBANKING&TRUSTCWASHINGTONMUTUALBANK', 'JPMORGANCHASEBANK,NAFIFTHTHIRDBANK', 'FRANKLINAMERICANMTGE', 'WELLSFARGOBANK,NAFIFTHTHIRDBANK', 'QUICKENLOANINC', 'USBANKNANATLCITYMTGECO', 'BANKOFAMERICA,NANATIONSTARMTGELLC', 'PENNYMACCORP', 'LAKEVIEWLOANSERVICINBRANCHBANKING&TRUSTC', 'PNCMTGESERVICES,INCNATIONSTARMTGELLC', 'NATIONSTARMTGELLCBACHOMELOANSERVICING', 'BRANCHBANKING&TRUSTCARVESTCENTRALMTGECO', 'BANKOFAMERICA,NACOUNTRYWIDE', 'BANKOFAMERICA,NABACHOMELOANSERVICING', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'FIFTHTHIRDMTGECO', 'Other servicers', 'BANKOFAMERICA,NAHOMESIDELENDING,INC', 'CENDANTMTGECORPORATIABNAMROMTGEGROUP,INC', 'BACHOMELOANSERVICINGNATIONSTARMTGELLC', 'DITECHFINANCIALLLC', 'PINGORALOANSERVICINGSUNTRUSTMORTGAGE,INC', 'PRINCIPALRESIDENTIALBRANCHBANKING&TRUSTC', 'CALIBERHOMELOANS,INCBANKOFAMERICA,NA', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'BANKOFAMERICA,NABAMORTGAGE,LLC', 'ARVESTCENTRALMTGECO', 'WELLSFARGOBANK,NAABNAMROMTGEGROUP,INC', 'GMACMTGECORPWELLSFARGOHOMEMORTGA', 'SUNTRUSTMORTGAGE,INC', 'BANKOFAMERICA,NA', 'ABNAMROMTGEGROUP,INC', 'PNCMTGESERVICES,INC', 'NATLCITYMTGECOBRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANKTAYLOR,BEAN&WHITAKER', 'CHASEHOMEFINANCELLCCITIMORTGAGE,INC', 'WASHINGTONMUTUALHOME', 'JPMORGANCHASEBANK,NA', 'FIFTHTHIRDBANK', 'ROUNDPOINTMTGESERVIC', 'BANKOFAMERICA,NAMETLIFEHOMELOANS,ADI', 'PNCMTGESERVICES,INCCITIMORTGAGE,INC', 'BRANCHBANKING&TRUSTCLAKEVIEWLOANSERVICIN', 'ALLYBANKFIFTHTHIRDMTGECO', 'WELLSFARGOBANK,NACITIMORTGAGE,INC', 'FIFTHTHIRDBANKFIFTHTHIRDMTGECO', 'UNIONSAVINGSBANKPHHMTGECORP', 'OLDKENTMTGECO', 'CHASEMANHATTANMTGECO', 'STEARNSLENDING,LLC', 'SENECAMTGESERVICING,PROVIDENTFUNDINGASSO', 'CALIBERHOMELOANS,INCNEWRESIDENTIALMTGELL', 'CALIBERHOMELOANS,INC', 'BACHOMELOANSERVICING', 'PHHMTGECORPSUNTRUSTMORTGAGE,INC', 'SUNTRUSTMORTGAGE,INCROUNDPOINTMTGESERVIC', 'COUNTRYWIDE', 'FTMTGESERVICES,INCWASHINGTONMUTUALBANK', 'BANKOFAMERICA,NAFLAGSTARCAPITALMARKE', 'GMACMTGECORP', 'CITIMORTGAGE,INCNATIONSTARMTGELLC', 'CHASEHOMEFINANCELLCJPMORGANCHASEBANK,NA', 'FREMONTBANK', 'PNCBANK,NATL', 'CITIMORTGAGE,INC', 'NATLCITYMTGECO', 'OCWENLOANSERVICING,L', 'FTMTGESERVICES,INC', 'CITIMORTGAGE,INCTAYLOR,BEAN&WHITAKER', 'PRINCIPALRESIDENTIALWASHINGTONMUTUALBANK', 'METLIFEHOMELOANS,ADI', 'PROVIDENTFUNDINGASSO', 'FRANKLINAMERICANMTGEBANKOFAMERICA,NA', 'CENDANTMTGECORPORATICOUNTRYWIDE', 'CHASEMTGECO', 'BRANCHBANKING&TRUSTC', 'CENTRALMTGECO', 'PNCMTGESERVICES,INCUSBANKNA', 'CALIBERHOMELOANS,INCQUICKENLOANINC', 'NATIONSTARMTGELLCOCWENLOANSERVICING,L', 'FLAGSTARCAPITALMARKE', 'PNCBANK,NATLPNCMTGESERVICES,INC', 'COUNTRYWIDEWELLSFARGOBANK,NA', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'BRANCHBANKING&TRUSTCFIFTHTHIRDBANK', 'PROVIDENTFUNDINGASSOROUNDPOINTMTGESERVIC', 'LAKEVIEWLOANSERVICINJPMORGANCHASEBANK,NA', 'NATLCITYMTGECOPNCMTGESERVICES,INC', 'GMACMTGECORPCHASEMANHATTANMTGECO', 'CITIMORTGAGE,INCBACHOMELOANSERVICING', 'CITIMORTGAGE,INCBRANCHBANKING&TRUSTC', 'UNIONSAVINGSBANK', 'SENECAMTGESERVICING,CALIBERHOMELOANS,INC', 'UNIONSAVINGSBANKJPMORGANCHASEBANK,NA', 'PROVIDENTFUNDINGASSOABNAMROMTGEGROUP,INC', 'WELLSFARGOBANK,NACOUNTRYWIDE', 'USBANKNAPNCBANK,NATL', 'PNCBANK,NATLABNAMROMTGEGROUP,INC', 'GMACMORTGAGE,LLC', 'ABNAMROMTGEGROUP,INCCENDANTMTGECORPORATI'],
        # 'seller_name': ['Other sellers', 'FT MORTGAGE COMPANIE', 'OLD KENT MORTGAGE CONATIONAL CITY MORTGA', 'FIRST UNION CAPITAL', 'FLEET MORTGAGE CORPOCROSSLAND MORTGAGE C', 'GMAC MORTGAGE CORPOR', 'ACCUBANC MORTGAGE CONORWEST MORTGAGE, IN', 'FLAGSTAR BANK, FSB', 'NATIONSBANC MORTGAGEHOMESIDE LENDING, IN', 'RESOURCE BANCSHARES', 'PRINCIPAL RESIDENTIACHASE MANHATTAN MORT', 'NAMCO ASSET MANAGEME', 'BANKAMERICA MORTGAGEPNC MORTGAGE CORPORA', 'G N MORTGAGE CORPORA', "WASHINGTON MUTUAL BASTANDARD FEDERAL BANBISHOP'S GATE RESIDENATIONSBANK, N.A.COUNTRYWIDE HOME LOA", 'Other sellers', 'NATIONAL CITY MORTGA', 'OLD KENT MORTGAGE COCROSSLAND MORTGAGE C', 'CHASE MANHATTAN MORT', 'FT MORTGAGE COMPANIEACCUBANC MORTGAGE CO', 'NORWEST MORTGAGE, IN', 'G N MORTGAGE CORPORABANK OF AMERICA, N.A', 'NATIONSBANC MORTGAGE', "FLAGSTAR BANK, FSBPRINCIPAL RESIDENTIABISHOP'S GATE RESIDEGE CAPITAL MORTGAGEFIRSTAR BANK, N.A.", 'PNC MORTGAGE CORPORA', 'ABN AMRO MORTGAGE GRCOUNTRYWIDE HOME LOA', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC', 'BANKOFAMERICA,NAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIALBISHOPSGATERESIDENTI', 'FTMTGECOMPANIES', 'GECAPITALMTGESERVICEFIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'NORWESTMORTGAGE,INC', 'BANKOFAMERICA,NAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'PRINCIPALRESIDENTIALBISHOPSGATERESIDENTI', 'FTMTGECOMPANIES', 'GECAPITALMTGESERVICEFIRSTARBANK,NA', 'PNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INCCOUNTRYWIDE', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CROSSLANDMTGECORPCHASEMANHATTANMTGECO', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCBISHOPSGATERESIDENTI', 'PRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOANPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEFIFTHTHIRDBANK', 'Other sellers', 'NATLCITYMTGECO', 'OLDKENTMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'WELLSFARGOHOMEMORTGAFLAGSTARBANK,FSB', 'BRANCHBANKING&TRUSTC', 'CROSSLANDMTGECORPPRINCIPALRESIDENTIAL', 'BISHOPSGATERESIDENTI', 'PNCMTGECORPOFAMERICAFIRSTARBANK,NA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCPRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN', 'BISHOPSGATERESIDENTIPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'OLDKENTMTGECO', 'NATLCITYMTGECO', 'CHASEMANHATTANMTGECOCOUNTRYWIDE', 'BANKOFAMERICA,NA', 'FLAGSTARBANK,FSBWELLSFARGOHOMEMORTGA', 'FIRSTARBANK,NA', 'BRANCHBANKING&TRUSTCPRINCIPALRESIDENTIAL', 'FIRSTHORIZONHOMELOAN', 'BISHOPSGATERESIDENTIPNCMTGECORPOFAMERICA', 'ABNAMROMTGEGROUP,INC', 'Other sellers', 'PROVIDENTFUNDINGASSO', 'TAYLOR,BEAN&WHITAKERABNAMROMTGEGROUP,INC', 'PRINCIPALRESIDENTIAL', 'WELLSFARGOHOMEMORTGAFLAGSTARBANK,FSB', 'SUNTRUSTMORTGAGE,INC', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA', 'USBANKNA', 'Other sellers', 'COUNTRYWIDE', 'PRINCIPALRESIDENTIALABNAMROMTGEGROUP,INC', 'GMACMTGECORP', 'WELLSFARGOHOMEMORTGA', 'USBANKNA', 'WELLSFARGOBANK', 'Other sellers', 'TAYLOR,BEAN&WHITAKERFIFTHTHIRDBANK', 'Other sellers', 'TAYLOR,BEAN&WHITAKER', 'CHASEMANHATTANMTGECOBRANCHBANKING&TRUSTC', 'Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA', 'Other sellers', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKER', 'USBANKNA', 'Other sellers', 'GMACMTGECORP', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKERPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'CHASEHOMEFINANCELLCUSBANKNA', 'FIFTHTHIRDBANK', 'ABNAMROMTGEGROUP,INC', 'WELLSFARGOCANKCNA', 'Other sellers', 'COUNTRYWIDE', 'TAYLOR,BEAN&WHITAKERABNAMROMTGEGROUP,INC', 'USBANKNA', 'FLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORPTAYLOR,BEAN&WHITAKER', 'USBANKNA', 'WASHINGTONMUTUALBANKFLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'GMACMTGECORPTAYLOR,BEAN&WHITAKER', 'USBANKNA', 'WASHINGTONMUTUALBANKFLAGSTARBANK,FSB', 'Other sellers', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDE', 'USBANKNABRANCHBANKING&TRUSTC', 'SOVEREIGNBANK', 'FIFTHTHIRDBANKWELLSFARGOBANK,NA', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKERCHASEHOMEFINANCELLC', 'Other sellers', 'COUNTRYWIDE', 'ABNAMROMTGEGROUP,INCPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'FIFTHTHIRDBANKGMACMTGECORP', 'TAYLOR,BEAN&WHITAKER', 'SOVEREIGNBANK', 'USBANKNAFLAGSTARCAPITALMARKE', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERGMACMORTGAGE,LLC', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERGMACMORTGAGE,LLC', 'Other sellers', 'USBANKNA', 'ABNAMROMTGEGROUP,INC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC', 'FIRSTHORIZONHOMELOANFIFTHTHIRDBANK', 'BRANCHBANKING&TRUSTC', 'WASHINGTONMUTUALBANKTAYLOR,BEAN&WHITAKER', 'BANKOFAMERICA,NA', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEPROVIDENTFUNDINGASSO', 'FIFTHTHIRDBANK', 'TAYLOR,BEAN&WHITAKERWASHINGTONMUTUALBANK', 'GMACMORTGAGE,LLC', 'ABNAMRO,NKACITIMORTG', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEFIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO', 'ABNAMRO,NKACITIMORTGTAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEFIRSTHORIZONHOMELOAN', 'PROVIDENTFUNDINGASSO', 'ABNAMRO,NKACITIMORTGTAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'FIFTHTHIRDBANK', 'UCBANCNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'COUNTRYWIDEGMACMORTGAGE,LLC', 'WASHINGTONMUTUALBANK', 'TAYLOR,BEAN&WHITAKERFLAGSTARCAPITALMARKE', 'FIRSTHORIZONHOMELOAN', 'Other sellers', 'USBANKNA', 'COUNTRYWIDE', 'FLAGSTARCAPITALMARKEGMACMORTGAGE,LLC', 'BRANCHBANKING&TRUSTC', 'TAYLOR,BEAN&WHITAKERWELLSFARGOBANK,NA', 'FIRSTHORIZONHOMELOAN', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDETAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'GMACMORTGAGE,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'COUNTRYWIDETAYLOR,BEAN&WHITAKER', 'FLAGSTARCAPITALMARKE', 'GMACMORTGAGE,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSOAMTRUSTBANK', 'FLAGSTARCAPITALMARKE', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'METLIFEHOMELOANS,ADI', 'PHHMTGECORP', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'UNIONSAVINGSBANK', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANKMETLIFEHOMELOANS,ADI', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'WELLSFARGOBANK,NABANKOFAMERICA,NA', 'UNIONSAVINGSBANK', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'AMTRUSTBANK', 'FIFTHTHIRDBANKMETLIFEHOMELOANS,ADI', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSOMETLIFEHOMELOANS,ADI', 'SUNTRUSTMORTGAGE,INC', 'BANKOFAMERICA,NAPHHMTGECORP', 'FREMONTBANK', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'PROVIDENTFUNDINGASSOUNIONSAVINGSBANK', 'METLIFEHOMELOANS,ADI', 'FIFTHTHIRDBANK', 'PHHMTGECORPBANKOFAMERICA,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'FIFTHTHIRDBANKPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'METLIFEHOMELOANS,ADIPHHMTGECORP', 'FREMONTBANK', 'JPMORGANCHASEBANK,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'UNIONSAVINGSBANKMETLIFEHOMELOANS,ADI', 'BANKOFAMERICA,NA', 'PHHMTGECORPPROVIDENTFUNDINGASSO', 'GMACMORTGAGE,LLC', 'FREMONTBANK', 'FIFTHTHIRDBANKJPMORGANCHASEBANK,NA', 'CITIMORTGAGE,INC', 'Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNAPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'UNIONSAVINGSBANKPHHMTGECORP', 'Other sellers', 'GUARANTEEDRATE,INC', 'BRANCHBANKING&TRUSTC', 'USBANKNAPROVIDENTFUNDINGASSO', 'BANKOFAMERICA,NA', 'UNIONSAVINGSBANKPHHMTGECORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GREENLIGHTFINANCIALSPROVIDENTFUNDINGASSO', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCPROVIDENTFUNDINGASSO', 'GREENLIGHTFINANCIALS', 'CALIBERFUNDINGLLCBANKOFAMERICA,NA', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'PROVIDENTFUNDINGASSO', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERFUNDINGLLC', 'PHHMTGECORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'GUARANTEEDRATE,INC', 'USBANKNACALIBERHOMELOANS,INC', 'UNITEDSHOREFINANCIAL', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA', 'PHHMTGECORP', 'CMGMORTGAGE,INCQUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLCSTEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS', 'PENNYMACCORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCCALIBERHOMELOANS,INC', 'BANKOFAMERICA,NA', 'PHHMTGECORP', 'CMGMORTGAGE,INCQUICKENLOANINC', 'FRANKLINAMERICANMTGE', 'LOANDEPOTCOM,LLCSTEARNSLENDING,INC', 'CHICAGOMTGESOLUTIONS', 'PENNYMACCORP', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'GUARANTEEDRATE,INCPHHMTGECORP', 'FIFTHTHIRDBANK', 'SUNTRUSTMORTGAGE,INCUNITEDSHOREFINANCIAL', 'BANKOFAMERICA,NA', 'CALIBERHOMELOANS,INCSTEARNSLENDING,INC', 'FLAGSTARBANK,FSB', 'LOANDEPOTCOM,LLCFRANKLINAMERICANMTGE', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STONEGATEMTGECORPSTEARNSLENDING,LLC', 'LOANDEPOTCOM,LLC', 'CALIBERHOMELOANS,INCGUARANTEEDRATE,INC', 'QUICKENLOANINC', 'PHHMTGECORPFRANKLINAMERICANMTGE', 'BANKOFAMERICA,NA', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,INGUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC', 'LOANDEPOTCOM,LLCSUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLCFLAGSTARBANK,FSB', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'PLAZAHOMEMORTGAGE,INGUARANTEEDRATE,INC', 'USBANKNA', 'CALIBERHOMELOANS,INC', 'LOANDEPOTCOM,LLCSUNTRUSTMORTGAGE,INC', 'QUICKENLOANINC', 'STEARNSLENDING,LLCFLAGSTARBANK,FSB', 'Other sellers', 'USBANKNA', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'USBANKNA', 'STEARNSLENDING,LLC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC', 'Other sellers', 'BRANCHBANKING&TRUSTC'],

        #     'st': ['NYAL', 'WA', 'CONY', 'WI', 'DENV', 'WV', 'LACT', 'ORMA', 'KSUT', 'WY', 'MAWA', 'MEOR', 'ARID', 'KYWV', 'IDHI', 'DEHI', 'UTWY', 'RI', 'WVSD', 'CAWV', 'GU', 'NVAR', 'CAUT', 'GAHI', 'GA', 'AZMN', 'OK', 'OH', 'TXSD', 'IDNC', 'SDUT', 'MENE', 'FLHI', 'OR', 'IAND', 'WAHI', 'TNKY', 'NJNV', 'NVDE', 'AKFL', 'HI', 'WYSD', 'IANY', 'PR', 'SCUT', 'MDOR', 'VTNE', 'ALND', 'GACT', 'TNID', 'PA', 'MICA', 'NJFL', 'IDDE', 'NJTX', 'COOR', 'NEKS', 'INPA', 'NEKY', 'SCKS', 'NEPA', 'AKLA', 'CAGA', 'VANJ', 'IAIN', 'ME', 'VTID', 'TXKS', 'WINY', 'MA', 'UT', 'MO', 'MN', 'MI', 'MTTN', 'MATX', 'MT', 'SDLA', 'MS', 'KYOH', 'SCMT', 'MSNM', 'FLNE', 'WINE', 'PAOR', 'COSD', 'ALAK', 'NHWY', 'ALAR', 'ORIN', 'MNNC', 'NCUT', 'VAKY', 'FL', 'INMO', 'NH', 'MAMI', 'NJ', 'AZ', 'NM', 'ARMO', 'NC', 'ND', 'NE', 'ID', 'WVDC', 'NY', 'NCMT', 'NVWY', 'IDLA', 'TXUT', 'FLUT', 'NV', 'NHVT', 'CO', 'CTWA', 'MD', 'CA', 'WVMT', 'MSVT', 'ORSC', 'WAPA', 'OKCO', 'MOIN', 'WVME', 'CT', 'UTNM', 'INUT', 'KS', 'VTOR', 'NYMN', 'NYMO', 'SC', 'MDNH', 'KY', 'AKHI', 'SD', 'NEWI', 'AZNM', 'TNOH', 'WVVA', 'DE', 'DC', 'TNTX', 'VARI', 'PRSD', 'AKSD', 'TXWV', 'TX', 'LA', 'NEFL', 'ARRI', 'KYNY', 'TN', 'IDVT', 'ORKS', 'NCMA', 'NCCT', 'WAIA', 'LAUT', 'CAMD', 'VA', 'AZIL', 'NDTX', 'NCTN', 'VI', 'AK', 'AL', 'TNWV', 'AR', 'VT', 'IL', 'UTHI', 'IN', 'IA', 'NEGA', 'INTX', 'MTAR', 'RIAR', 'AKSC', 'LAMD', 'WVMI', 'WACA', 'RIAZ', 'NJAL', 'NJAK', 'ALKY', 'COOH', 'NMHI', 'ILWI', 'WVGA']
        # }
