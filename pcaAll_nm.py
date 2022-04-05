import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import os

PATH = 'G:/nhr/fMRI/timeseries'

cols = ['x', 'y', 'z'] + list(range(0, 105))


for sub in os.listdir(PATH):
    tmp_path = PATH + '/' + sub
    #print(filename)
    for roi in os.listdir(tmp_path):
        #print(roi)
        file_name = tmp_path + '/' + roi
        df = pd.read_csv(file_name, names=cols, sep=' ')

        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        data = df.to_numpy()
        data = np.swapaxes(data, 1, 0)

        scaler = MinMaxScaler()
        data_rescaled = scaler.fit_transform(data)
        pca = PCA(n_components = .75)
        pca.fit(data)
        reduced = pca.transform(data)

        print(data.shape)
        print(reduced.shape)

        out_path = 'G:/nhr/fMRI/output' + '/' + roi
        out_df = pd.DataFrame(reduced.T)
        out_df.to_csv(out_path)

