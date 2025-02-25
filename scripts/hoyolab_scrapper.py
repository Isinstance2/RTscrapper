#!/usr/bin/env python
# coding: utf-8

# In[19]:


import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from save_utils import save_data
from dotenv import load_dotenv
import os


# In[20]:


env_file_path = 'E:/RTscrapper/config/.env'
load_dotenv(os.path.join(env_file_path))

COOKIE_PATH = os.getenv('COOKIE_PATH')
LOGS_DATA_DIR = os.getenv('LOGS_DATA_DIR')
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR')
PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')


# In[21]:


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.hoyolab.com/")
    time.sleep(10)
    
    try:
        with open(COOKIE_PATH, 'r') as f:
            cookies = json.load(f)
            
        for cookie in cookies:
            if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                del cookie["sameSite"]
            
            driver.add_cookie(cookie)
        
        driver.refresh()
        time.sleep(5)
        print("✅ Successfully logged in using session cookies!")
        
    except Exception as e:
        print(f"❌ Error loading cookies: {e}")
        driver.quit()  # If cookies load fails, close the driver

    return driver


# In[22]:


def scrape_hoyolab(driver):
    driver.get("https://act.hoyolab.com/app/community-game-records-sea/rpg/index.html?bbs_presentation_style=fullscreen&gid=6&user_id=157229845&utm_source=hoyolab&utm_medium=gamecard&bbs_theme=dark&bbs_theme_device=1#/hsr")
    
    time.sleep(30)
    
    character_containers = driver.find_elements("css selector", "div.c-hrd-sa-wrapper")
    
    character_stats_list = []
    
    for container in character_containers:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", container)
            driver.execute_script("arguments[0].click();", container)
            time.sleep(3)
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract character name
            char_name = soup.find("p", class_="c-hrd-ri-name").text.strip()
            
            # Extract character stats
            stats_blocks = soup.find_all("div", class_="c-hrdcs-item")
            char_stats = {"name": char_name}
            
            for block in stats_blocks:
                stat_name = block.find("span", class_="c-hrdcs-name").text.strip()
                stat_value = block.find("span", class_="c-hrdcs-num").text.strip()
                char_stats[stat_name] = stat_value  # Store stat as column
                
            # Append character stats to the list
            character_stats_list.append(char_stats)
                
        except Exception as e:
            print(f"⚠️ Error simulating click: {e}")
                
                
    df = pd.DataFrame(character_stats_list)
    
    if not df.empty:
        print('Scrapped data has been added as a df!')
        return df
    else:
        print('Unable to use scrapped data as a df')
        
    
    
    
    driver.quit()
    
    


# In[23]:


driver = init_driver()
df = scrape_hoyolab(driver)


# In[24]:


save_data(df, 'Scrapped_data.csv', folder_type='raw', file_format='csv')


# In[ ]:




