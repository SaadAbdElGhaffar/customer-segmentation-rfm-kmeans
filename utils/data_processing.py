import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_data(file_path):
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    return df

def clean_data(df):
    df.dropna(subset=['CustomerID'], inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[~df['InvoiceNo'].str.startswith('C')]
    df = df[~df['StockCode'].str.contains('^[a-zA-Z]', regex=True)]
    df = df[~((df['Description'] == 'Next Day Carriage') | (df['Description'] == 'High Resolution Image'))]
    df = df[df['UnitPrice'] > 0]
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df

def prepare_rfm_data(df):
    df["Date"] = pd.to_datetime(df["InvoiceDate"])
    reference_date = max(df["Date"]) + pd.DateOffset(days=1)
    recency = (reference_date - df.groupby('CustomerID')["Date"].max()).dt.days
    recency.name = "Recency"
    frequency = df.groupby('CustomerID')['Date'].count()
    frequency.name = "Frequency"
    monetary = df.groupby('CustomerID')['TotalPrice'].sum()
    monetary.name = "Monetary"
    
    recency_df = recency.reset_index()
    recency_df.columns = ['CustomerID', 'Recency']
    frequency_df = frequency.reset_index()
    frequency_df.columns = ['CustomerID', 'Frequency']
    monetary_df = monetary.reset_index()
    monetary_df.columns = ['CustomerID', 'Monetary']
    
    rfm = recency_df.merge(frequency_df, on="CustomerID").merge(monetary_df, on="CustomerID")
    rfm = rfm.set_index('CustomerID')
    return rfm

def transform_rfm_data(rfm):
    rfm['Recency'] = np.log1p(rfm['Recency'])
    rfm['Frequency'] = np.log1p(rfm['Frequency'])
    rfm['Monetary'] = np.log1p(rfm['Monetary'])
    return rfm

def remove_outliers_iqr(rfm, columns=['Frequency', 'Monetary']):
    for col in columns:
        Q1 = rfm[col].quantile(0.25)
        Q3 = rfm[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        rfm = rfm[(rfm[col] >= lower_bound) & (rfm[col] <= upper_bound)]
    return rfm