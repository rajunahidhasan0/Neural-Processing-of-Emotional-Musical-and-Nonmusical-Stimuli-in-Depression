import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

cols = ['x', 'y', 'z'] + list(range(0, 105))
df = pd.read_csv('swarsub-control01/swarsub-control01-FrontalMedialCortex.csv', names=cols, sep=' ')

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
# print(reduced)
# df = pd.DataFrame(reduced.T)
# print(df.head())

with open("../PCs/out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(reduced.T)
