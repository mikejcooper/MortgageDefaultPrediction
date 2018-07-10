import numpy as np
import pandas as pd

class ModelDataGenerator:
    """ A class that generates data for model. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """

    def load_data(self, data, activeTargetClass):
        self._data = self._format_dataset(data, activeTargetClass)
        self._set_data()

    def _format_dataset(self, df, target_class):
        assert isinstance(df, pd.DataFrame)
        labels = df[target_class].values
        df = df.drop(target_class, axis=1)
        data = df.values
        data = pd.DataFrame(data)
        for column in data:
            # if not one-hot-encoded
            if 1 != (data[column].max() - data[column].min()):
                data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())

        # Remove nan values
        data = data.fillna(0)
        return (np.array(data), labels)

    def _set_data(self):
        self._train_size = len(self._data[0])
        self._input_length = len(self._data[0][0])
        self._class_count = len(self._data[1][0])

    def getData(self):
        return (self._data[0], self._data[1])

    def shuffle_data(self):
        self._train = self.unison_shuffled_copies(self._train[0] , self._train[1])
        self._validation = self.unison_shuffled_copies(self._validation[0] , self._validation[1])

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return (a[p], b[p])

