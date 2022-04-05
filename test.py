import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import os

PATH = 'G:/nhr/fMRI/timeseries'

cols = ['x', 'y', 'z'] + list(range(0, 105))
# X=[]
# Y=[]
m=39
n=48
subj= np.zeros((m, n))
nf= np.zeros((m, n))
nt= np.zeros((m, n))
et= np.zeros((m, n))
sf= np.zeros((m, n))

# print(' sub ==== 95% ==== 90% ==== 80% ==== 75%')
# print('----------------------------')
sb=0
for sub in os.listdir(PATH):
    tmp_path = PATH + '/' + sub
    # print('')
    ind=int(0)
    for roi in sorted(os.listdir(tmp_path)):
        #print(roi)
        file_name = tmp_path + '/' + roi
        df = pd.read_csv(file_name, names=cols, sep=' ')

        df = df.drop(df.columns[[0, 1, 2]], axis=1)
        data = df.to_numpy()
        data = np.swapaxes(data, 1, 0)

        scaler = MinMaxScaler()
        data_rescaled = scaler.fit_transform(data)
        pca = PCA(n_components = .95)
        pca.fit(data_rescaled)
        reduced = pca.transform(data_rescaled)
        tmp=reduced.shape[1]
        # print(ind,' ==== ',tmp)
        if(reduced.shape[1]>=15):
            scaler = MinMaxScaler()
            data_rescaled = scaler.fit_transform(data)
            pca = PCA(n_components = .90)
            pca.fit(data_rescaled)
            reduced = pca.transform(data_rescaled)
            ninty = reduced.shape[1]

            scaler = MinMaxScaler()
            data_rescaled = scaler.fit_transform(data)
            pca = PCA(n_components = .80)
            pca.fit(data_rescaled)
            reduced = pca.transform(data_rescaled)
            eighty = reduced.shape[1]

            scaler = MinMaxScaler()
            data_rescaled = scaler.fit_transform(data)
            pca = PCA(n_components = .75)
            pca.fit(data_rescaled)
            reduced = pca.transform(data_rescaled)

            nf[sb][ind]=tmp
            nt[sb][ind]=ninty
            et[sb][ind]=eighty
            sf[sb][ind]=reduced.shape[1]
        subj[sb][ind]=ind+1
        ind=ind+1   
    # print('Processing subject: ', sb+1)
    sb=sb+1

print(' sub ==== 95% ==== 90% ==== 80% ==== 75%')
for i in range(39):
    print('#Subject ====', i+1)
    for j in range(48):
        # line_new = '{:>3} {:>8}  {:>7} {:>8} {:>8}'.format(subj[i][j], nf[i][j], nt[i][j], et[i][j], sf[i][j])
        print("%3d %8d %7d %8d %8d"%(subj[i][j], nf[i][j], nt[i][j], et[i][j], sf[i][j]))
        # print(line_new)
        # npca.insert(line_new)
    print('*********************************************************')
