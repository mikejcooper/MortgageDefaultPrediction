import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Playground:
    """ A class that parses input data from file. """

    def __init__(self):
        """ Example of docstring on the __init__ method.  """


        # self.ml_model(data_frame)

    def ml_model(self,df_credit):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

        # Excluding the missing columns
        # del df_credit["Saving accounts"]
        # del df_credit["Checking account"]

        y = df_credit["Risk_good"].values

        df_credit.drop('Risk_good', axis=1, inplace=True)
        df_credit.drop('Risk_bad', axis=1, inplace=True)
        X = df_credit.values

        print self._dataFrame.dtypes



        # Spliting X and y into train and test version
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # Creating the classifier
        model = RandomForestClassifier(n_estimators=10, random_state=0, class_weight="balanced_subsample", )

        # Running the fit
        model.fit(X_train, y_train)

        # Printing the Training Score
        print("Training score data: ")
        print(model.score(X_train, y_train))

        # Testing the model
        # Predicting by X_test
        y_pred = model.predict(X_test)

        # Verificaar os resultados obtidos
        print(accuracy_score(y_test, y_pred))
        print("\n")
        print(confusion_matrix(y_test, y_pred))
        print("\n")
        print(classification_report(y_test, y_pred))



    def show_heat_map_corr(self, df):

        assert isinstance(df, pd.DataFrame)

        plt.figure(figsize=(14, 12))
        df.corr()
        sns.heatmap(df.corr(), linewidths=0.1, vmax=1.0,
                    square=True, linecolor='white', annot=True)
        plt.show()


if __name__ == "__main__":
    Playground()
    print("hello world")

