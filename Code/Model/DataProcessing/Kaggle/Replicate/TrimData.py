import FeatureIndex


def drop_null_columns(data):
    """Drop columns (most of values are null)"""
    data.drop(FeatureIndex.null_cols, axis=1, inplace=True)
    return None


def drop_emp_title(data):
    data.drop('emp_title', axis=1, inplace=True)
    return None


def drop_url(data):
    data.drop('url', axis=1, inplace=True)
    return None


def drop_zip_code(data):
    data.drop('zip_code', axis=1, inplace=True)
    return None

def drop_earliest_cr_line(data):
    data.drop('earliest_cr_line', axis=1, inplace=True)
    return None

def drop_out_prncp(data):
    data.drop('out_prncp', axis=1, inplace=True)
    return None

def drop_out_prncp_inv(data):
    data.drop('out_prncp_inv', axis=1, inplace=True)
    return None

def drop_total_rec_late_fee(data):
    data.drop('total_rec_late_fee', axis=1, inplace=True)
    return None

def drop_recoveries(data):
    data.drop('recoveries', axis=1, inplace=True)
    return None

def drop_collection_recovery_fee(data):
    data.drop('collection_recovery_fee', axis=1, inplace=True)
    return None

def drop_last_pymnt_d(data):
    data.drop('last_pymnt_d', axis=1, inplace=True)
    return None

def drop_collections_12_mths_ex_med(data):
    data.drop('collections_12_mths_ex_med', axis=1, inplace=True)
    return None

def drop_policy_code(data):
    data.drop('policy_code', axis=1, inplace=True)
    return None

def drop_application_type(data):
    data.drop('application_type', axis=1, inplace=True)
    return None


def drop_acc_now_delinq(data):
    data.drop('acc_now_delinq', axis=1, inplace=True)
    return None

def drop_tot_cur_bal(data):
    data.drop('tot_cur_bal', axis=1, inplace=True)
    return None

def drop_tot_coll_amt(data):
    data.drop('tot_coll_amt', axis=1, inplace=True)
    return None

def drop_pymnt_plan(data):
    data.drop('pymnt_plan', axis=1, inplace=True)
    return None

def drop_title(data):
    data.drop('title', axis=1, inplace=True)
    return None

def drop_issue_d(data):
    data.drop('issue_d', axis=1, inplace=True)
    return None

def drop_addr_state(data):
    data.drop('addr_state', axis=1, inplace=True)
    return None

def drop_last_credit_pull_d(data):
    data.drop('last_credit_pull_d', axis=1, inplace=True)
    return None

def split_loan_in_progress(data):
    """Return table of loan in progress. It drops the loan in progress from loan data internally."""
    progress_bool = data.loan_status.isin(FeatureIndex.in_progress_index)
    loan_in_progress = data[progress_bool].drop('loan_status', axis=1)
    data.drop(list(loan_in_progress.index), axis=0, inplace=True)
    return loan_in_progress


def categorize_target(data):
    """Returns encoded loan status: Safe, Warning and Bad"""

    def func(x):
        if x['loan_status'] in FeatureIndex.bad_index:
            return 0
        elif x['loan_status'] in FeatureIndex.warning_index:
            return 1
        else:
            return 2

    data['loan_status_encoded'] = data.apply(func, axis=1)
    data.drop('loan_status', axis=1, inplace=True)
    return data


def ext_num_from_sub_grade(data):
    data['sub_grade'] = data['sub_grade'].map(lambda x: int(x.lstrip('ABCDEFG')))
    return data


def fill_na_annual_inc(data):
    data.annual_inc.fillna(data.annual_inc.median(), inplace=True)
    return None


def fill_na_title(data):
    data.title.fillna('Unknown', inplace=True)
    return None

def fill_na_delinq_2yrs(data):
    data.delinq_2yrs.fillna(data.delinq_2yrs.median(), inplace=True)
    return None

def fill_na_inq_last_6mths(data):
    data.inq_last_6mths.fillna(data.inq_last_6mths.median(), inplace=True)
    return None

def fill_na_open_acc(data):
    data.open_acc.fillna(data.open_acc.median(), inplace=True)
    return None

def fill_na_pub_rec(data):
    data.pub_rec.fillna(data.pub_rec.median(), inplace=True)
    return None

def fill_na_revol_util(data):
    data.revol_util.fillna(data.revol_util.median(), inplace=True)
    return None

def fill_na_total_acc(data):
    data.total_acc.fillna(data.total_acc.median(), inplace=True)
    return None

def fill_na_last_credit_pull_d(data):
    data.last_credit_pull_d.fillna('Unknown', inplace=True)
    return None

def fill_na_total_rev_hi_lim(data):
    data.total_rev_hi_lim.fillna(data.total_rev_hi_lim.median(), inplace=True)
    return None