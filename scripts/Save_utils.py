#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import pandas as pd

def create_folder_if_not_exists(folder_path):
    # Debugging: Print the folder path
    print(f"Checking if folder exists: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"Creating folder: {folder_path}")
        os.makedirs(folder_path)

def save_data(data, filename, folder_type='raw', file_format='csv'):
    base_data_folder = 'E:/RTscrapper/data'  # Update this path if necessary
    
    # Define folder paths for different types of data
    folder_paths = {
        'raw': os.path.join(base_data_folder, 'raw'),
        'processed': os.path.join(base_data_folder, 'processed'),
        'logs': os.path.join(base_data_folder, 'logs')
    }
    
    # Check if folder type exists, else use 'raw' by default
    folder_path = folder_paths.get(folder_type, folder_paths['raw'])
    
    # Create folder if it doesn't exist
    create_folder_if_not_exists(folder_path)
    
    # Construct the full file path
    file_path = os.path.join(folder_path, f"{filename}.{file_format}")
    
    # Debugging: Check the final file path
    print(f"Final file path: {file_path}")
    
    # Save data based on the file format
    if file_format == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    elif file_format == 'csv':
        if isinstance(data, pd.DataFrame):
            data.to_csv(file_path, index=False)
        else:
            raise ValueError('Data must be a pandas DataFrame for CSV format.')
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
            
    print(f"Data saved to {file_path}")
    
    



# In[ ]:




