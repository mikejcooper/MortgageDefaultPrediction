import platform

def get_run_name():
    import datetime
    now = datetime.datetime.now()
    return str(now.day) + "_" + str(now.hour) + ":" + str(now.minute)

def get_dataset_name():
    if GERMAN_DATA:
        return "German"
    elif KAGGLE_DATA:
        return "Kaggle"
    elif AMERICAN_DATA:
        return "American"
    else:
        return "Unknown"

def get_log_dir():
    if platform.system() == 'Darwin':
        return '{cwd}/../../Data/logs/'
    else:
        return '/mnt/storage/home/mc14641/Thesis/Data/logs/'

GERMAN_DATA = False
KAGGLE_DATA = False
AMERICAN_DATA = True

CURRENT_DESCRIPTION = get_dataset_name() + "_" + get_run_name() + "_MAIN_"


BATCH_SIZE = 64
# BATCH_SIZE = 4096


MULTI_LABEL = False
GOOD_BAD_LABEL = True
PREPAID_RATIO = False




