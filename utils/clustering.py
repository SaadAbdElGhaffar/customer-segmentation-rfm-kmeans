import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def perform_clustering(rfm_data, n_clusters=4):
    std_scaler = StandardScaler()
    df_scaled = std_scaler.fit_transform(rfm_data[['Recency', 'Frequency', 'Monetary']])
    df_scaled = pd.DataFrame(df_scaled, columns=['Recency', 'Frequency', 'Monetary'])
    df_scaled.index = rfm_data.index
    
    inertia = []
    score = []
    for i in range(2, 15):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)
        score.append(silhouette_score(df_scaled, kmeans.labels_))
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df_scaled)
    
    rfm_clustered = rfm_data.copy()
    rfm_clustered['Cluster'] = kmeans.labels_
    
    cluster_label = {0: 'At Risk', 1: 'Champions', 2: 'Loyal Customers', 3: 'New Customers'}
    rfm_clustered['Cluster_Labels'] = rfm_clustered['Cluster'].map(cluster_label)
    
    return rfm_clustered, kmeans, std_scaler, cluster_label