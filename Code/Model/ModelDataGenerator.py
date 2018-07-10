import datetime
import platform
import random
from multiprocessing import Process, Manager
import time

import numpy as np
import pandas as pd
import sys
from imblearn.over_sampling import SMOTE
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_predict
from sklearn.svm import SVC
from skmultilearn.problem_transform import LabelPowerset
from imblearn.over_sampling import RandomOverSampler
from DataGenerator import DataGenerator as DataGenerator
import DataProcessing.American.Globals as Globals
from DataProcessing.American.DataParser import DataParser


class ModelDataGenerator:
    """ A class that generates data for model. """

    MULTI_BATCH = False
    UPSAMPLING = False
    DOWNSAMPLE = True
    UPSAMPLING_ALL = False

    def __init__(self, Load_Data=True):
        """ Example of docstring on the __init__ method.  """
        # (self._train, self._validation) = self._create_train_validation_datasets(DataGenerator().ActiveDataset, DataGenerator().ActiveTargetClass)
        if platform.system() == 'Darwin':
            self.current_dataset_index = -2
        else:
            self.current_dataset_index = 40
            # self.MULTI_BATCH = True


        if Load_Data:
            df_OHE = DataParser()._read_HDFStore_OHE(self.current_dataset_index)
            self.load_data(df_OHE, DataGenerator().ActiveTargetClass)
            # self.load_data(DataGenerator().ActiveDataset_i(self.current_dataset_index), DataGenerator().ActiveTargetClass)

        # (self._train, self._validation) = self.feature_ranking(self._train, self._validation)

        # self.Logistic_regression(self._train, self._validation)
        # self.Linear_regression(self._train, self._validation)
        # self.random_forest(self._train, self._validation)
        # self.SVM(self._train, self._validation)
        # self.MLP(self._train, self._validation)


    def load_data(self, data, activeTargetClass):

        (self._train, self._validation) = self._create_train_validation_datasets(data, activeTargetClass)
        self.shuffle_data()
        print("Size: " + str(float((sys.getsizeof(self._train[0]) + sys.getsizeof(self._train[1])) / 1000.0)) + " mb")
        self._set_data()




    @property
    def input_length(self):
        return self._input_length

    @property
    def class_count(self):
        return self._class_count

    @property
    def training_size(self):
        return self._train_size

    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, value):
        self._batch_size = value

    def _format_dataset(self, df, target_class):
        assert isinstance(df, pd.DataFrame)
        labels = df[target_class].values
        if Globals.GERMAN_DATA:
            labels = labels - 1
            # one hot a list of integers
            one_hot_labels = np.eye(np.max(labels) + 1)[labels]
            labels = one_hot_labels
        # remove first column - full of 0's
        # if Globals.GERMAN_DATA:
        #     one_hot_labels = np.delete(one_hot_labels, np.s_[0:1], axis=1)

        df = df.drop(target_class, axis=1)
        data = df.values
        # Standardise features
        # data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
        # data = (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))

        data = pd.DataFrame(data)

        for column in data:
            # if not one-hot-encoded
            if 1 != (data[column].max() - data[column].min()):
                #             data[column] = (data[column] - data[column].mean()) / data[column].std()
                data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())

        # Remove nan values
        data = data.fillna(0)

        # data = data.loc[:, 30:42]

        return (np.array(data), labels)

    def _create_train_validation_datasets(self, df, target_class):
        assert isinstance(df, pd.DataFrame)
        training_set_size = 0.8 * len(df)
        random.seed(len(df) + datetime.datetime.now().day + 1)
        # print(len(df) + datetime.datetime.now().day)
        # random.seed(len(df))
        df = shuffle(df)
        sudo_ran_sample = [random.randint(1, len(df)) for i in range(1, len(df))]
        msk = np.array(sudo_ran_sample) < training_set_size

        (train_data, train_labels) = self._format_dataset(df.iloc[msk], target_class)
        (validation_data, validation_labels) = self._format_dataset(df.iloc[~msk], target_class)

        if self.UPSAMPLING:
            (train_data, train_labels) = self.upsample_training_data(train_data, train_labels)

        if self.DOWNSAMPLE:
            (train_data, train_labels) = self.downsample_training_data(train_data, train_labels)
            (validation_data, validation_labels) =  self.downsample_training_data(validation_data, validation_labels)

        if self.UPSAMPLING_ALL:
            (train_data, train_labels) = self.upsample_training_data(train_data, train_labels)
            # (train_data, train_labels) = self.downsample_training_data(train_data, train_labels)
            (validation_data, validation_labels) =  self.upsample_training_data(validation_data, validation_labels)

        # Shuffle dataset?????

        # Shuffle dataset?????

        self.print_class_ratios(train_labels, "Training Class ratios BEFORE")
        self.print_class_ratios(validation_labels, "Validation Class ratios BEFORE")

        return ((train_data, train_labels) , (validation_data, validation_labels))

    def _set_data(self):
        self._train_size = len(self._train[0])
        self._input_length = len(self._train[0][0])
        self._class_count = len(self._train[1][0])
        self._batch_size = Globals.BATCH_SIZE
        self._train_batch_count = 0
        self._validation_batch_count = 0
        self._train_batch_indexes = range(0, len(self._train[0]), self._batch_size)
        self._validation_batch_indexes = range(0, len(self._validation[0]), self._batch_size)
        # Think about random shuffling of indexes?
        if self.MULTI_BATCH:
            self._fetch_next_dataset()

    def _batch_generator(self, dataset, batch_indexes, i):
        if(len(batch_indexes) < 2):
            return np.array(dataset[0]), np.array(dataset[1])

        return np.array(dataset[0][batch_indexes[i]:batch_indexes[i+1]]), np.array(dataset[1][batch_indexes[i]:batch_indexes[i+1]])

    def shuffle_data(self):
        self._train = self.unison_shuffled_copies(self._train[0] , self._train[1])
        self._validation = self.unison_shuffled_copies(self._validation[0] , self._validation[1])


    def get_data(self):
        return (np.array(self._train[0]) , np.array(self._train[1]))

    def _check_multi_batch(self):
        # If next batch is a cycle
        if self._train_batch_count + 1 >= len(self._train_batch_indexes):
            self.shuffle_data()
            if not self.MULTI_BATCH:
                return
            self._switch_data()



    def _switch_data(self):
        print "WAITING ON DATA"
        print
        self._fetch_data_process.join()
        # raw_input("Press Enter to continue...")
        (self._train2, self._validation2) = self._shared_data_store[0]
        (self._train, self._validation) = (self._train2, self._validation2)
        self.current_dataset_index = (self.current_dataset_index + 1) % DataGenerator().Number_Of_Datasets
        self._set_data()

    def _fetch_next_dataset(self):
        self._shared_data_store = Manager().dict()
        next_data_set = (self.current_dataset_index + 1) % DataGenerator().Number_Of_Datasets
        self._fetch_data_process = Process(target=self._fetch_dataset, args=(next_data_set, self._shared_data_store))
        self._fetch_data_process.start()


    def _fetch_dataset(self, i, store):
        df_OHE = DataParser()._read_HDFStore_OHE(i)
        store[0] = self._create_train_validation_datasets(df_OHE, DataGenerator().ActiveTargetClass)
        store[0] = (self._train, self._validation)
        # store[0] = self._create_train_validation_datasets(DataGenerator().ActiveDataset_i(i), DataGenerator().ActiveTargetClass)
        print "NEW Dataset : " + str(i) + ", length : " + str(len(store[0][0][0]))

    def getTrainBatch(self, allowSmallerBatches=False):
        self._check_multi_batch()
        if self._train_batch_count + 1 >= len(self._train_batch_indexes):
            self._train_batch_count = 0
        batch = self._batch_generator(self._train, self._train_batch_indexes, self._train_batch_count)
        self._train_batch_count += 1
        return batch

    def getValidationBatch(self, allowSmallerBatches=False):
        if self._validation_batch_count + 1 >= len(self._validation_batch_indexes):
            self._validation_batch_count = 0
        batch = self._batch_generator(self._validation, self._validation_batch_indexes, self._validation_batch_count)
        self._validation_batch_count += 1
        return batch

    def feature_ranking(self, training, validation):

        training_data, training_labels = (training[0], training[1])
        validation_data, validation_labels = (validation[0], validation[1])
        # plot feature importance using built-in function
        from xgboost import XGBClassifier
        # split data into X and y
        X = training_data
        y = training_labels
        yt = LabelPowerset().transform(training_labels)
        # fit model no training data
        model = XGBClassifier()
        model.fit(X, yt)
        f_scores = model.feature_importances_

        training_data_pruned = training_data
        validation_data_pruned = validation_data
        f_scores_sorted = -np.sort(-f_scores)
        threshold_top_percentage = 0.3
        threshold = f_scores_sorted[int(f_scores_sorted.shape[0] * threshold_top_percentage)]
        for i in range(0, len(f_scores)):
            if f_scores[i] < threshold:
                i_dif = training_data.shape[1] - training_data_pruned.shape[1]
                if i == 0:
                    training_data_pruned = training_data_pruned[:,1:]
                    validation_data_pruned = validation_data_pruned[:,1:]
                elif i == len(f_scores) - 1:
                    training_data_pruned = training_data_pruned[:, :i - i_dif]
                    validation_data_pruned = validation_data_pruned[:, :i - i_dif]
                else:
                    training_data_pruned = np.column_stack((training_data_pruned[:, 0:i - i_dif], training_data_pruned[:, i - i_dif +1:]))
                    validation_data_pruned = np.column_stack((validation_data_pruned[:, 0:i - i_dif], validation_data_pruned[:, i - i_dif +1:]))

        print training_data_pruned.shape

        return ((training_data_pruned,training_labels), (validation_data_pruned, validation_labels))

    def downsample_training_data(self, data, labels):
        from imblearn.under_sampling import NeighbourhoodCleaningRule, ClusterCentroids
        start_time = time.time()

        ratio = 1

        df = pd.DataFrame(data=labels, columns=['label_0', 'label_1'])
        pos_indexes = df.loc[df['label_0'] == 0].index
        neg_indexes = df.loc[df['label_0'] == 1].index
        remove_num = int(len(neg_indexes) * ratio)
        indexes_to_remove = pos_indexes[0:-remove_num]

        data = np.delete(data, indexes_to_remove,0)
        labels = np.delete(labels, indexes_to_remove,0)

        print("--- Resampling Took : %s seconds ---" % (time.time() - start_time))


        return data, labels



    def upsample_training_data(self, data, labels):
        start_time = time.time()

        data = pd.DataFrame(data=data)
        labels = pd.DataFrame(data=labels)

        column_i = labels.ix[:, 0]
        indexes_equal_1 = np.where(column_i == 1)
        mask = np.ones(np.max(indexes_equal_1[0]) + 1, dtype=bool)  # np.ones_like(a,dtype=bool)
        mask[indexes_equal_1[0]] = True

        data_good_loans = data.iloc[~mask]
        labels_good_loans = labels.iloc[~mask]

        data = data.iloc[mask]
        labels = labels.iloc[mask]

        UPSAMPLE_RATIO = 1.0 # 1 = 50:50 equal split

        # ---- Step 1 - Randomly oversample -----

        ros = RandomOverSampler(random_state=42)
        yt = LabelPowerset().transform(labels)
        # Applies the above stated multi-label (ML) to multi-class (MC) transformation.
        # X_resampled, y_resampled = ros.fit_sample(data, yt)
        X_resampled, y_resampled = SMOTE(kind='borderline1').fit_sample(data, yt)

        # Inverts the ML-MC transformation to recreate the ML set
        y_resampled = np.eye(np.max(y_resampled) + 1)[y_resampled]

        # class_count = len(labels.ix[:, 0])
        # majority_class_index = class_count.index(max(class_count))
        majority_class_count = len(labels.ix[:, 0]) - len(indexes_equal_1)
        desired_samples = int(majority_class_count * UPSAMPLE_RATIO)
        required_samples = desired_samples - len(indexes_equal_1)

        data_additional = np.concatenate((data_good_loans, X_resampled[0:required_samples]))
        data = np.concatenate((data, data_additional))
        labels_additional = np.concatenate((labels_good_loans, y_resampled[0:required_samples]))
        labels = np.concatenate((labels, labels_additional))


        # ---- Step 2 - Collect minority class data from oversamples -----

        # class_count = [None] * labels.shape[1]
        # for i in range(0,labels.shape[1]):
        #     class_count[i] = np.count_nonzero(labels[:,i] == 1)
        #     if class_count[i] == 0:
        #         zeros =  y_resampled[:, 0:1]
        #         zeros[:, 0] = 0
        #         left = y_resampled[:, 0:i+1]
        #         right = y_resampled[:, i+1:]
        #         y_resampled = np.column_stack((left, zeros, right))
        #
        # majority_class_index = class_count.index(max(class_count))
        # majority_class_count = max(class_count)
        #
        #
        # for i in range(0,labels.shape[1]):
        #     if i != majority_class_index and class_count[i] != 0:
        #         column_i = y_resampled[:,i]
        #         indexes_equal_1 = np.where(column_i == 1)
        #
        #         data_class_i = X_resampled[indexes_equal_1]
        #         labels_class_i = y_resampled[indexes_equal_1]
        #
        #         desired_samples = int(majority_class_count * UPSAMPLE_RATIO)
        #         required_samples = desired_samples - class_count[i]
        #
        #         if required_samples < 0:
        #             print("Increase UPSAMPLE_RATIO")
        #         else:
        #             data = np.concatenate((data, data_class_i[0:required_samples]))
        #             labels = np.concatenate((labels, labels_class_i[0:required_samples]))

        (data, labels) = self.unison_shuffled_copies(data, labels)

        print("--- Resampling Took : %s seconds ---" % (time.time() - start_time))

        return data, np.array(labels)

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return (a[p], b[p])

    # def upsample_all(self, data, labels):
    #
    #     # ---- Step 1 - Randomly oversample -----
    #
    #     ros = RandomOverSampler(random_state=42)
    #     yt = LabelPowerset().transform(labels)
    #     # Applies the above stated multi-label (ML) to multi-class (MC) transformation.
    #     X_resampled, y_resampled = ros.fit_sample(data, yt)
    #     X_resampled, y_resampled = SMOTE(kind='borderline1').fit_sample(data, yt)
    #
    #     # ros = RandomOverSampler(random_state=43)
    #     # X_resampled, y_resampled = ros.fit_sample(X_resampled, y_resampled)
    #     # Inverts the ML-MC transformation to recreate the ML set
    #     y_resampled = np.eye(np.max(y_resampled) + 1)[y_resampled]
    #
    #     df = pd.DataFrame(data=[X_resampled, np.array(y_resampled)], columns=['x', 'y'])
    #     df = shuffle(df)
    #
    #
    #
    #     return df['x'], df['y']


    def Logistic_regression(self, train, validation):
        from sklearn import model_selection
        from sklearn.linear_model import LogisticRegression

        X = np.concatenate((train[0], validation[0]))
        Y = np.concatenate((train[1], validation[1]))
        Y = LabelPowerset().transform(Y)

        seed = 7
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        model = LogisticRegression()
        scoring = 'accuracy'
        results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        print("LogR Accuracy: %.3f") % (results.mean())

    def Linear_regression(self, train, validation):
        from sklearn.linear_model import LinearRegression

        X = np.concatenate((train[0], validation[0]))
        Y = np.concatenate((train[1], validation[1]))
        Y = LabelPowerset().transform(Y)

        model = LinearRegression()
        predictions = cross_val_predict(model, X, Y, cv=6)

        accuracy = metrics.r2_score(Y, predictions)
        print("LinR Accuracy: %.3f ") % (accuracy)

    def random_forest(self, train, validation):
        train_x, test_x, train_y, test_y = train[1], validation[1], train[0], validation[0]
        train_y = LabelPowerset().transform(train_y)
        test_y = LabelPowerset().transform(test_y)

        # Create random forest classifier instance
        clf = RandomForestClassifier()
        trained_model = clf.fit(train_x, train_y)
        predictions = trained_model.predict(test_x)

        # Train and Test Accuracy
        # print "Train Accuracy :: ", accuracy_score(train_y, trained_model.predict(train_x))
        # print "Test Accuracy  :: ", accuracy_score(test_y, predictions)
        print("RF Accuracy: %.3f ") % (accuracy_score(test_y, predictions))

    def SVM(self, train, validation):
        train_x, test_x, train_y, test_y = train[1], validation[1], train[0], validation[0]
        train_y = LabelPowerset().transform(train_y)
        test_y = LabelPowerset().transform(test_y)

        # Create SVM classifier instance
        # print self.svc_param_selection(train_x, train_y, 5)
        clf = SVC(C=0.001, gamma=0.001)
        trained_model = clf.fit(train_x, train_y)
        predictions = trained_model.predict(test_x)

        # Train and Test Accuracy
        print("SVM Accuracy: %.3f ") % accuracy_score(test_y, predictions)

    def svc_param_selection(self, X, y, nfolds):
        Cs = [0.001, 0.01, 0.1, 1, 10]
        gammas = [0.001, 0.01, 0.1, 1]
        param_grid = {'C': Cs, 'gamma': gammas}
        grid_search = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=nfolds)
        grid_search.fit(X, y)
        grid_search.best_params_
        return grid_search.best_params_

    def MLP(self, train, validation):
        from sklearn.neural_network import MLPClassifier
        train_x, test_x, train_y, test_y = train[1], validation[1], train[0], validation[0]
        train_y = LabelPowerset().transform(train_y)
        test_y = LabelPowerset().transform(test_y)

        # Create SVM classifier instance
        clf = MLPClassifier()
        trained_model = clf.fit(train_x, train_y)
        predictions = trained_model.predict(test_x)

        # Train and Test Accuracy
        print("MLP Accuracy: %.3f ") % accuracy_score(test_y, predictions)


    def print_class_ratios(self, labels, print_str):
        class_count = [None] * labels.shape[1]
        for i in range(0, labels.shape[1]):
            class_count[i] = np.count_nonzero(labels[:, i] == 1)

        majority_class_count = max(class_count)

        class_ratio_str = print_str + ",  " + str(float(class_count[0]) / float(labels.shape[0]) * 100)
        for i in range(1, len(class_count)):
            a = float(class_count[i]) / float(majority_class_count)
            class_ratio_str += " : " + str(float(class_count[i]) / float(labels.shape[0]) * 100)

        class_count_str = print_str + ",  " + str(float(class_count[0]))
        for i in range(1, len(class_count)):
            a = float(class_count[i]) / float(majority_class_count)
            class_count_str += " : " + str(float(class_count[i]))

        print class_ratio_str
        print class_count_str + "(raw numbers)"



if __name__ == "__main__":
    ModelDataGenerator()
    print("hello world")

