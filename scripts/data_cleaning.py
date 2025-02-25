#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from dotenv import load_dotenv
import os
from Save_utils import save_data


# In[2]:


env_file_path = 'E:/RTscrapper/config/.env'
load_dotenv(os.path.join(env_file_path))

RAW_DATA = os.getenv('RAW_DATA_DIR')
PROCESSED_DATA = os.getenv('PROCESSED_DATA_DIR')


# In[3]:


df = pd.read_csv(f"{RAW_DATA}/Scrapped_data.csv")
df


# In[4]:


df = df.drop(columns='Unnamed: 0')
df = df.rename(columns={'name' : 'Name'})
df.head(5)


# In[5]:


df.dtypes


# In[6]:


for col in df.iloc[:, 5:19]:
    df[col] = df[col].astype('str').str.replace('%', "", regex=False)
    df[col] = df[col].astype(float)
    df[col] = df[col] / 100
    
df.head(5)


# In[7]:


duplicates = df[df.duplicated()]
print(duplicates)


# In[8]:


print(df.isnull().sum())


# In[9]:


print(df['Name'].unique())


# In[10]:


save_data(df, 'processed_data', 'processed', 'csv')

