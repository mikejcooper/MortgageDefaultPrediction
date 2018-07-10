from TrimData import ext_num_from_sub_grade
from TrimData import drop_emp_title
from TrimData import fill_na_annual_inc
from TrimData import drop_zip_code
from TrimData import fill_na_delinq_2yrs
from TrimData import drop_earliest_cr_line
from TrimData import fill_na_inq_last_6mths
from TrimData import fill_na_open_acc
from TrimData import fill_na_pub_rec
from TrimData import fill_na_revol_util
from TrimData import fill_na_total_acc
from TrimData import drop_out_prncp
from TrimData import drop_out_prncp_inv
from TrimData import drop_total_rec_late_fee
from TrimData import drop_recoveries
from TrimData import drop_collection_recovery_fee
from TrimData import drop_last_pymnt_d
from TrimData import drop_collections_12_mths_ex_med
from TrimData import drop_policy_code
from TrimData import drop_application_type
from TrimData import drop_acc_now_delinq
from TrimData import drop_tot_coll_amt
from TrimData import drop_tot_cur_bal
from TrimData import fill_na_total_rev_hi_lim
from TrimData import drop_url
from TrimData import drop_pymnt_plan
from TrimData import drop_issue_d
from TrimData import drop_addr_state
from TrimData import drop_last_credit_pull_d


def trim_features(loan):
    ext_num_from_sub_grade(loan)
    drop_emp_title(loan)
    fill_na_annual_inc(loan)
    drop_zip_code(loan)
    fill_na_delinq_2yrs(loan)
    drop_earliest_cr_line(loan)
    fill_na_inq_last_6mths(loan)
    fill_na_open_acc(loan)
    fill_na_pub_rec(loan)
    fill_na_revol_util(loan)
    fill_na_total_acc(loan)
    drop_pymnt_plan(loan)
    drop_url(loan)
    drop_total_rec_late_fee(loan)
    drop_out_prncp(loan)
    drop_out_prncp_inv(loan)
    drop_recoveries(loan)
    drop_collection_recovery_fee(loan)
    drop_last_pymnt_d(loan)
    drop_collections_12_mths_ex_med(loan)
    drop_policy_code(loan)
    drop_application_type(loan)
    drop_acc_now_delinq(loan)
    drop_tot_coll_amt(loan)
    drop_tot_cur_bal(loan)
    fill_na_total_rev_hi_lim(loan)
    drop_issue_d(loan)
    drop_addr_state(loan)
    drop_last_credit_pull_d(loan)