#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from Save_utils import save_data
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq


# In[2]:


file_path = 'E:/RTscrapper/config/.env'
load_dotenv(os.path.join(file_path))

PROCESSED_DATA = os.getenv('PROCESSED_DATA_DIR')
SECRET_KEY = os.getenv('SECRET_KEY')


# In[3]:


df = pd.read_csv(f"{PROCESSED_DATA}/processed_data.csv")
df.head()


# In[4]:


print(df.describe())


# In[5]:


fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(df['CRIT Rate'], bins=10, kde=True, ax=axes[0])
axes[0].set_title('CRIT Rate Distribution')

sns.histplot(df['CRIT DMG'], bins=10, kde=True, ax=axes[1])
axes[1].set_title('CRIT DMG Distribution')

plt.show()


# In[6]:


df['CRIT ratio'] = df['CRIT Rate'] / df['CRIT DMG']
df.head()


# In[7]:


sns.boxplot(x=df['CRIT ratio'])
plt.title('CRIT Ratio outliers')
plt.show()


# In[8]:


def remove_outliers(df):
    df_cleaned = df.copy()  
    
    for column in df_cleaned.select_dtypes(include=['float64', 'int64']):
        Q1 = df_cleaned[column].quantile(0.25)
        Q3 = df_cleaned[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
    df_cleaned = df_cleaned[(df_cleaned[column] >= lower) & (df_cleaned[column] <= upper)]
    
    return df_cleaned


# In[9]:


model_df = remove_outliers(df)

model_df['Name'] = model_df['Name'].astype('string')


print(model_df['Name'].dtype)


save_data(model_df, 'model_df', 'processed', 'csv')


# In[10]:


df_filtered = df[(df['CRIT Rate'] > 0.4) & (df['CRIT DMG'] > 1.0)].copy()

# Compute CRIT Ratio for the filtered dataset
df_filtered['CRIT Ratio'] = df_filtered['CRIT DMG'] / df_filtered['CRIT Rate']

# Sort characters by CRIT Ratio in descending order
df_sorted = df_filtered.sort_values(by='CRIT Ratio', ascending=False)

# Display top crit characters
print('Best DPS Characters:')
print(df_sorted[['Name', 'CRIT Rate', 'CRIT DMG', 'CRIT Ratio']])


# In[11]:


print("Skewness:\n", df[['CRIT Rate', 'CRIT DMG', 'CRIT ratio']].skew())
print("\nKurtosis:\n", df[['CRIT Rate', 'CRIT DMG', 'CRIT ratio']].kurtosis())


# In[12]:


corr_matrix = df.corr(numeric_only=True)
corr_matrix 


# In[13]:


sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
plt.title('Corr Heatmap')

plt.show()


# ## Meta Build Analysis: Understanding the Correlations Between Key Stats
# 
# n HSR, players often optimize their characters by prioritizing certain stats that best complement their desired playstyle. While every player’s build may differ based on character roles (DPS, support, tank, etc.), meta builds (i.e., the most effective and popular builds based on game mechanics) emerge as common trends that are highly correlated with performance.
# 
# 
# #### Key Findings:
# 
# 
# 
# CRIT DMG and Elemental DMG Correlation
# 
# There is often a positive correlation between CRIT DMG and Elemental DMG for many DPS builds. Players frequently aim to optimize CRIT DMG while also focusing on Elemental DMG to enhance their overall performance in elemental reactions (like Vaporize or Melt).
# This suggests that for optimal DPS output, players tend to increase both CRIT DMG and Elemental DMG, which are both key contributors to maximizing damage, especially when exploiting elemental weaknesses.
# 

# In[14]:


fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(df['DEF'], bins=10, kde=True, ax=axes[0])
axes[0].set_title('DEF Distribution')

sns.histplot(df['ATK'], bins=10, kde=True, ax=axes[1])
axes[1].set_title('ATK Distribution')

plt.show()


# In[15]:


stats = ['ATK', 'DEF', 'HP', 'CRIT Rate', 'CRIT DMG']

fig, axes = plt.subplots(len(stats), 1, figsize=(8, 15))

for i, stat in enumerate(stats):
    sns.histplot(df[stat], bins=20, kde=True, ax=axes[i])
    axes[i].set_title(f'Distribution of {stat}')
    axes[i].set_xlabel(stat)
    axes[i].set_ylabel('Number of Characters')

plt.tight_layout()
plt.show()


# In[16]:


model_df.dtypes


# In[ ]:




