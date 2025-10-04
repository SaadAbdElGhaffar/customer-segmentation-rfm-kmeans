import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle
import os

class CustomerSegmentationPredictor:
    def __init__(self, kmeans_model=None, scaler=None):
        self.kmeans_model = kmeans_model
        self.scaler = scaler
        self.cluster_labels = {0: 'At Risk', 1: 'Champions', 2: 'Loyal Customers', 3: 'New Customers'}

    def load_models(self, models_dir="outputs/models"):
        try:
            with open(f"{models_dir}/kmeans_model.pkl", "rb") as f:
                self.kmeans_model = pickle.load(f)
            
            with open(f"{models_dir}/scaler.pkl", "rb") as f:
                self.scaler = pickle.load(f)
            
            with open(f"{models_dir}/cluster_labels.pkl", "rb") as f:
                self.cluster_labels = pickle.load(f)
            
            print(f"Models loaded from {models_dir}/")
        except FileNotFoundError as e:
            print(f"Model files not found: {e}")
            print("Please run main.py first to train the models.")

    def preprocess_input(self, recency, frequency, monetary):
        log_recency = np.log1p(recency)
        log_frequency = np.log1p(frequency)
        log_monetary = np.log1p(monetary)
        features = np.array([[log_recency, log_frequency, log_monetary]])
        if self.scaler is not None:
            features = self.scaler.transform(features)
        return features

    def predict_cluster(self, recency, frequency, monetary):
        if self.kmeans_model is None:
            raise ValueError("Model not loaded. Please call load_models() first.")
        features = self.preprocess_input(recency, frequency, monetary)
        cluster = self.kmeans_model.predict(features)[0]
        return cluster

    def predict_segment(self, recency, frequency, monetary):
        cluster = self.predict_cluster(recency, frequency, monetary)
        return self.cluster_labels.get(cluster, f"Cluster {cluster}")

def customer_segmentation(Recency, Frequency, Monetary, kmeans_model, scaler, cluster_labels):
    data_recency = np.log1p(Recency)
    data_frequency = np.log1p(Frequency)
    data_monetary = np.log1p(Monetary)
    data = pd.DataFrame({'Recency': [data_recency], 'Frequency': [data_frequency], 'Monetary': [data_monetary]})
    X_data = scaler.transform(data)
    pred = kmeans_model.predict(X_data)
    return cluster_labels[pred[0]]

def predict_from_saved_models(recency, frequency, monetary):
    predictor = CustomerSegmentationPredictor()
    predictor.load_models()
    return predictor.predict_segment(recency, frequency, monetary)

if __name__ == "__main__":
    try:
        segment = predict_from_saved_models(5, 7, 100)
        print(f"Customer segment: {segment}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to run main.py first to generate the models.")