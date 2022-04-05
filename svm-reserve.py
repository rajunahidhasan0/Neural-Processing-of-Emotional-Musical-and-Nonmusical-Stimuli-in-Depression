import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd
import csv
import os

PATH1 = 'G:/nhr/fMRI/signal/train'
PATH2 = 'G:/nhr/fMRI/signal/test'
cols = ['x', 'y', 'z'] + list(range(0, 105))

m=48
n=39
train_vect = np.empty((0, 105), int)
for sub in os.listdir(PATH1):
    tmp_path = PATH1 + '/' + sub
    # reg=0
    for roi in os.listdir(tmp_path):

        file_name = tmp_path + '/' + roi
        df = pd.read_csv(file_name, names=cols, sep=' ')

        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        data = df.to_numpy()
        data = np.swapaxes(data, 1, 0).T
        b = data[:20, :105]

        train_vect = np.append(train_vect, b, axis=0)
        # reg=reg+1
        # ind=ind+1
        break

# print(train_vect)


test_vect = np.empty((0, 105), int)
for sub in os.listdir(PATH2):
    tmp_path = PATH2 + '/' + sub
    # reg=0
    for roi in os.listdir(tmp_path):

        file_name = tmp_path + '/' + roi
        df = pd.read_csv(file_name, names=cols, sep=' ')

        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        data = df.to_numpy()
        data = np.swapaxes(data, 1, 0).T
        b = data[:20, :105]

        test_vect = np.append(test_vect, b, axis=0)
        # reg=reg+1
        # ind=ind+1
        break

print(train_vect.shape)
print(test_vect.shape)
# train_vect.shape, test_vect.shape

# cols = train_vect.columns
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train = scaler.fit_transform(train_vect)
X_test = scaler.transform(test_vect)
# X_train = pd.DataFrame(X_train, columns=[cols])
# X_test = pd.DataFrame(X_test, columns=[cols])
X_train = pd.DataFrame(X_train)
X_test = pd.DataFrame(X_test)
# X_train.describe()

# print(X_train.describe())

# import SVC classifier
from sklearn.svm import SVC

# import metrics to compute accuracy
from sklearn.metrics import accuracy_score

# instantiate classifier with default hyperparameters
svc=SVC() 

# fit classifier to training set
y_train=np.zeros(30)
# y_train = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# np.append(y_train, np.ones(15), axis=0)

# print(y_train.shape)

svc.fit(X_train,y_train)

# # make predictions on test set
# y_pred=svc.predict(X_test)

# # compute and print accuracy score
# print('Model accuracy score with default hyperparameters: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))