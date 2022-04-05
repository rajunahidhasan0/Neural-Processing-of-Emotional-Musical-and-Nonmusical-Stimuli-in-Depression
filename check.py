import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import os

PATH = 'G:/nhr/fMRI/timeseries'

cols = ['x', 'y', 'z'] + list(range(0, 105))

cnt=[0,0,0,0,0,0]

for sub in os.listdir(PATH):
    tmp_path = PATH + '/' + sub
    #print(filename)

    # cnt[0]=0
    # cnt[1]=0
    # cnt[2]=0
    # cnt[3]=0
    # cnt[4]=0
    # cnt[5]=0
    dir = "G:/nhr/fMRI/PCs"
    path = os.path.join(dir, sub)

    for roi in os.listdir(tmp_path):
        #print(roi)
        file_name = tmp_path + '/' + roi
        df = pd.read_csv(file_name, names=cols, sep=' ')

        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        data = df.to_numpy()
        data = np.swapaxes(data, 1, 0)

        scaler = MinMaxScaler()
        data_rescaled = scaler.fit_transform(data)
        pca = PCA(n_components = .95)
        pca.fit(data)
        reduced = pca.transform(data)

        # print(data.shape[1], reduced.shape[1])
        
        if(reduced.shape[1]>5):
            print('What is happpennnig',reduced.shape[1])
        else:
            cnt[reduced.shape[1]]=cnt[reduced.shape[1]]+1
        # print(reduced.shape)

    
    print(cnt[0])
    print(cnt[1])
    print(cnt[2])
    print(cnt[3])
    print(cnt[4])
    print(cnt[5])
    print('------------------------------------------------------------------')