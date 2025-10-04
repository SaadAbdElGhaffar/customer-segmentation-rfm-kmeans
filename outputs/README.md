# Outputs Directory

This directory contains all generated files from the customer segmentation analysis.

## Generated Files:

### CSV Results:
- `rfm_segments.csv` - Individual customer RFM scores and segments
- `clustered_segments.csv` - Customer cluster assignments and labels

### Models (in models/ subdirectory):
- `kmeans_model.pkl` - Trained K-means clustering model
- `scaler.pkl` - StandardScaler used for feature normalization
- `cluster_labels.pkl` - Mapping of cluster numbers to segment names

### Plots (in plots/ subdirectory):
- Various visualization files will be saved here if plotting functions are added

## Usage:
These files are automatically generated when you run `main.py`. The models can be loaded using the `prediction.py` module for making predictions on new customers.