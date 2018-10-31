# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import json
from mysql.connector import Error

from sklearn.cluster import KMeans


# In[2]:


#query company data in SQL

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password",
      database="leadbook"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM company")


    col_names = [i[0] for i in mycursor.description]

    results = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    # Make the result in Pandas DataFrame

    df = pd.DataFrame(data = results, columns = col_names)
    
except Error as e:
    raise Exception(e)


# In[3]:


f1 = df['revenue'].values
plt.scatter(f1, f1, c='black', s=7)


# In[4]:


X = np.array(df['revenue'].astype(float)).reshape(-1, 1)


# In[5]:


kmeans = KMeans(n_clusters=3)
kmeans.fit(X)


# In[6]:


#Cluster companies by revenue

cluster = []
for i in range(len(X)):
    predict_me = np.array(X[i].astype(float))
    predict_me = predict_me.reshape(-1, len(predict_me))
    cluster.append(kmeans.predict(predict_me)[0])


# In[7]:


#Create cluster label

centroids = list(kmeans.cluster_centers_)

min_index = centroids.index(min(centroids))
max_index = centroids.index(max(centroids))

label = ['medium size company','medium size company','medium size company']
label[min_index] = 'small scale company'
label[max_index] = 'large scale company'

df['cluster'] = cluster
df['cluster_label'] = 'medium size company'


df.loc[df['cluster'] == min_index, 'cluster_label'] = label[min_index]
df.loc[df['cluster'] == max_index, 'cluster_label'] = label[max_index]


# In[8]:


#plot the label on every observation

for i in range(0, len(cluster)):
    if cluster[i] == 0:
        c1 = plt.scatter(df['revenue'][i],df['revenue'][i],c='r', marker='+')
    elif cluster[i] == 1:
        c2 = plt.scatter(df['revenue'][i],df['revenue'][i],c='g', marker='o')
    elif cluster[i] == 2:
        c3 = plt.scatter(df['revenue'][i],df['revenue'][i],c='b', marker='*')
plt.legend([c1, c2, c3], label)
plt.title('Company dataset with 3 clusters by revenue using K-Means')
plt.show()


# In[9]:


#TASK 2.3
#plot the boundaries

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = 100000     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = df['revenue'].min() - 1, df['revenue'].max() + 1
y_min = x_min
y_max = x_max
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(xx.ravel().reshape(-1, 1))

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(df['revenue'], df['revenue'], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:], centroids[:],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means decision boundary by company revenue\n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.show()


# In[10]:


#TASK 2.1
#plot cluster label and number of companies in each group
sns.set(style="darkgrid")
ax = sns.countplot(x="cluster_label", data=df)
plt.title('Cluster label and number of companies in each group')
plt.show()


# In[11]:


#TASK 2.2
#plot cluster label and number of companies for each country
fig, (ax1,ax2,ax3) =plt.subplots(1,3,figsize=(25,10))
plt.title('Cluster label and number of companies for each country')
sns.countplot(x="cluster_label", data=df.loc[df['country'] == 'Malaysia'], ax=ax1)
ax1.set_title('Malaysia')
sns.countplot(x="cluster_label", data=df.loc[df['country'] == 'Singapore'], ax=ax2)
ax2.set_title('Singapore')
sns.countplot(x="cluster_label", data=df.loc[df['country'] == 'Hongkong'], ax=ax3)
ax3.set_title('Hongkong')
plt.show()
