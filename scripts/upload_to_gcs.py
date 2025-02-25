#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from google.cloud import storage
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
import pandas_gbq 


# In[2]:


file_path = 'E:/RTscrapper/config/.env'
load_dotenv(os.path.join(file_path))

PROCESSED_DATA = os.getenv('PROCESSED_DATA_DIR')
SECRET_KEY = os.getenv('SECRET_KEY')


# In[3]:


BUCKET_NAME = 'hsr_data'
DESTINATION_BLOB_NAME = 'hsr_stats.csv'


# In[4]:


credentials = service_account.Credentials.from_service_account_file(SECRET_KEY)
storage_client = storage.Client(credentials=credentials)


# In[5]:


import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
import pandas_gbq

def upload_csv_to_gcs_and_bigquery(df: pd.DataFrame, bucket_name: str, destination_blob_name: str, bq_table: str, project_id: str):
    """Uploads a DataFrame to GCS as CSV and then loads it into BigQuery."""
    
    try:
        
        csv_data = df.to_csv(index=False, encoding='utf-8')
        
        
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        
        
        blob.upload_from_string(csv_data, content_type="text/csv")
        print(f"✅ CSV uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")
    
    except Exception as e:
        print(f"❌ GCS Upload ERROR: {str(e)}")
        return

    try:
        
        pandas_gbq.to_gbq(df,destination_table=bq_table, 
                           project_id=project_id, 
                           if_exists='replace') 
        
        print(f"✅ Data loaded into BigQuery table: {bq_table}")
    
    except Exception as e:
        print(f"❌ BigQuery ERROR: {str(e)}")



# In[6]:


df = pd.read_csv(f"{PROCESSED_DATA}/model_df.csv")

upload_csv_to_gcs_and_bigquery(df, 
                               bucket_name='hsr_data', 
                               destination_blob_name='hsr_stats.csv',
                               bq_table='hsr-stats001.hsr_dataset.hsr_stats',
                               project_id='hsr-stats001')
    


# In[7]:


df.dtypes


# In[8]:


df.head()


# In[ ]:




