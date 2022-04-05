import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import os

PATH = 'G:/nhr/fMRI/timeseries'

cols = ['x', 'y', 'z'] + list(range(0, 105))
X=[]
Y=[]
ind=1
print(' sub ==== 95% ==== 90% ==== 80% ==== 75%')
# print('----------------------------')
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

            line_new = '{:>3} {:>8}  {:>7} {:>8} {:>8}'.format(ind, tmp, ninty, eighty, reduced.shape[1])
            print(line_new)
            # print(ind, '   ',tmp, ' <====> ',ninty, ' <====> ',reduced.shape[1])


        
        X.append(ind)
        Y.append(reduced.shape[1])
        ind=ind+1


        # plt.plot(reduced.shape)
        # plt.show()


        out_path = 'G:/nhr/fMRI/output' + '/' + roi
        out_df = pd.DataFrame(reduced.T)
        break
        #out_df.to_csv(out_path)

# print(dt)
plt.rcParams["figure.figsize"] = [4.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Plot bar chart with data points
plt.bar(X, Y)

# Display the plot
plt.show()
