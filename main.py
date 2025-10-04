import os
import pickle
from utils.data_processing import load_data, clean_data, prepare_rfm_data, transform_rfm_data, remove_outliers_iqr
from utils.rfm_analysis import calculate_rfm_scores, segment_customers
from utils.clustering import perform_clustering

def main():
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/models", exist_ok=True)
    
    df = load_data("data/data.csv")
    df_clean = clean_data(df)
    rfm = prepare_rfm_data(df_clean)
    rfm = transform_rfm_data(rfm)
    rfm = remove_outliers_iqr(rfm)
    
    rfm_segments = calculate_rfm_scores(rfm)
    rfm_segments = segment_customers(rfm_segments)
    
    rfm_clustered, kmeans_model, scaler, cluster_labels = perform_clustering(rfm)
    
    rfm_segments.to_csv("outputs/rfm_segments.csv", index=False)
    rfm_clustered.to_csv("outputs/clustered_segments.csv")
    
    with open("outputs/models/kmeans_model.pkl", "wb") as f:
        pickle.dump(kmeans_model, f)
    
    with open("outputs/models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    with open("outputs/models/cluster_labels.pkl", "wb") as f:
        pickle.dump(cluster_labels, f)
    
    print("Analysis completed. Results saved in outputs/ directory.")

if __name__ == "__main__":
    main()