import sys
from sklearn import datasets
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import scatter_matrix
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import seaborn as sb
from sklearn.naive_bayes import GaussianNB
import os
os.chdir("C:\\Directory")
df = pd.read_csv("Annexure_1_result.csv")
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.info()
df.describe()
scatter_matrix(df, figsize=(15, 10))
plt.show()
df.head()
predict_df = df.drop(["Text_id", "Sampled_date", "T_site",
                      "T_plant", "Sampling_point", "Condition"], axis=1)
X = predict_df.drop(["Fault"], axis=1)
y = predict_df["Fault"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1)
model = []
model.append(('LR', LogisticRegression()))
model.append(('LDA', LinearDiscriminantAnalysis()))
model.append(('KNN', KNeighborsClassifier()))
model.append(('DTC', DecisionTreeClassifier()))
model.append(('GNB', GaussianNB()))
model.append(('SVC', SVC()))
seed = 6
scoring = "accuracy"
for name, mod in model:
    kfold = KFold(n_splits=3, random_state=seed)
    cv_result = cross_val_score(
        mod, X_train, y_train, cv=kfold, scoring=scoring)
    print("Model: {}, Mean: {} and std: {}".format(
        name, cv_result.mean(), cv_result.std()))
for name, mod in model:
    mod.fit(X_train, y_train)
    prediction = mod.predict(X_test)
    val = accuracy_score(y_test, prediction)
    print("The model is {} and Accuracy: {}".format(name, val))
