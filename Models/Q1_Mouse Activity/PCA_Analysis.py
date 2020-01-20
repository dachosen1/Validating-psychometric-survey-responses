import os

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors as knn

os.getcwd()
df = pd.read_csv('df_model.csv')

# data preprocessing
df1 = pd.DataFrame()
df1 = df.replace([np.inf, -np.inf], np.nan).dropna()
df2 = df1.loc[:, ~df1.columns.isin(['validation', 'user_id', 'system'])]

corrmat = df1.corr()
sns.heatmap(corrmat)

# normalize the data
# perform PCA
from sklearn.decomposition import PCA

pca = PCA(n_components = 2)
X_pca = pca.fit_transform(X)

# plot PC1 and PC2
plt.scatter(X_pca.T[0], X_pca.T[1], alpha = 0.75, c = 'red')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

principalDf = pd.DataFrame(data = X_pca
                           , columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, df1[['validation', 'user_id']]], axis = 1)

# Plot PCA result with validation added
fig = plt.figure(figsize = (8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('PCA with 2 Components', fontsize = 20)
validations = [1, 0]
colors = ['r', 'g']
for validation, color in zip(validations, colors):
    indicesToKeep = finalDf['validation'] == validation
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(validations)
ax.grid()

distortions = []  # sum of squared error within the each cluster
for i in range(1, 20):
    km = KMeans(n_clusters = i,
                init = 'k-means++',
                n_init = 10,
                max_iter = 300,
                random_state = 0)
    km.fit(X_pca)
    distortions.append(km.inertia_)

plt.plot(range(1, 20), distortions, marker = 'o', alpha = 0.75)
plt.xlabel('Number of clusters')
plt.ylabel('Distortions')
plt.show()

# K- means
from sklearn.cluster import KMeans

# Kmeans using pca results
km = KMeans(n_clusters = 2,
            init = 'k-means++',
            n_init = 10,
            max_iter = 300,
            tol = 1e-04,
            random_state = 0)

y_km = km.fit_predict(X_pca)

# plot K-means result
plt.scatter(X_pca[y_km == 0, 0],
            X_pca[y_km == 0, 1],
            c = 'lightgreen',
            label = 'Cluster 1')
plt.scatter(X_pca[y_km == 1, 0],
            X_pca[y_km == 1, 1],
            c = 'orange',
            label = 'Cluster 2')
plt.scatter(km.cluster_centers_[:, 0],
            km.cluster_centers_[:, 1],
            s = 85,
            alpha = 0.75,
            marker = 'o',
            c = 'black',
            label = 'Centroids')

plt.legend(loc = 'best')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# get the users per each cluster

km_clust = pd.DataFrame(km.labels_, columns = ['km_label'])

# 0 is cluster 1
# 1 is cluster 2

km_clust['user_id'] = df1['user_id'].values
km_clust['validation'] = df1['validation'].values
km_clust['km_label'].value_counts()

# KNN for each PCA Data Point


knn_class = knn(n_neighbors = 10)
y_knn = knn_class.fit(X_pca)

distances, indices = y_knn.kneighbors(X_pca)

# knn distance plot to determine DBSCAN eps
distanceDec = sorted(distances[:, 10 - 1], reverse = True)
plt.plot(indices[:, 0], distanceDec)

# DBSCAN
from sklearn.cluster import DBSCAN

dbs = DBSCAN(eps = 0.04,
             min_samples = 5)

y_dbs = dbs.fit_predict(X_pca)

# plot DB-SCAN results
plt.scatter(X_pca[y_dbs == -1, 0],
            X_pca[y_dbs == -1, 1],
            c = 'lightgreen',
            label = 'Cluster 1')
plt.scatter(X_pca[y_dbs == 0, 0],
            X_pca[y_dbs == 0, 1],
            c = 'orange',
            label = 'Cluster 2')
plt.scatter(X_pca[y_dbs == 1, 0],
            X_pca[y_dbs == 1, 1],
            c = 'lightblue',
            label = 'Cluster 3')
plt.legend(loc = 'best')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# get the users per each cluster

dbs_clust = pd.DataFrame(dbs.labels_, columns = ['dbs_label'])

# -1 is cluster 1
# 0 is cluster 2
# 1 is cluster 3

dbs_clust['user_id'] = df1['user_id'].values
dbs_clust['validation'] = df1['validation'].values
dbs_clust['dbs_label'].value_counts()

X = preprocessing.normalize(df1)
