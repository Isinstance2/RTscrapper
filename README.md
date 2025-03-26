# RTscrapper: Automated Web Scraping & Data Cleaning

## Overview

RTscrapper automates the extraction of character data from the Hoyoverse platform, cleans and transforms the data, and uploads it to Google Cloud Storage (GCS) and BigQuery for analysis and visualization. The project consists of the following components:

* Web Scraping: Collects character data from the Hoyoverse platform (Hoyolab).

* Data Cleaning: Processes and cleans the scraped data by removing outliers and applying necessary transformations.

* Data Upload: Uploads cleaned data to Google Cloud Storage (GCS).



This project streamlines the entire workflow of web scraping, data processing, and storage while allowing for future scalability to additional platforms or data sources.

## Project Structure

```
RTscrapper/
│── data/
│   ├── raw/              # Stores raw scraped data
│   ├── process/          # Stores processed/cleaned data
│── scripts/
│   ├── hoyolab_scrapper.py     # Scrapes character data from Hoyoverse (Hoyolab)
│   ├── data_cleaning.py        # Cleans and processes the scraped data
│   ├── descriptive_data.py     # Generates summary statistics and analysis
│   ├── upload_to_gcs.py        # Uploads cleaned data to Google Cloud Storage
│   ├── Save_utils.py           # Utility functions for saving data (CSV, JSON, GCS upload)
│── requirements.txt            # Dependencies
│── README.md                   # Project documentation

```

## Installation
1. Clone repository
```
git clone https://github.com/Isistance2/RTscrapper.git
cd RTscrapper
```

2. Set Up Virtual Environment (Optional but Recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set Up Credentials

This project requires authentication for Google Cloud and Hoyoverse scraping:

* Google Cloud: Create a service account and download the JSON key file.

* Hoyoverse Cookies: Export your Hoyoverse session cookies to authenticate the scraper.

* Save credentials as environment variables or in a .env file.

## Automation

1. Automating Scraping, Cleaning, and Upload

Using Python script:
```
import subprocess

print("Starting data pipeline...")

# Run each script sequentially
subprocess.run(["python", "scripts/hoyolab_scrapper.py"])
subprocess.run(["python", "scripts/data_cleaning.py"])
subprocess.run(["python", "scripts/upload_to_gcs.py"])

print("Pipeline execution completed!")

```
Run it with:
```
python run_pipeline.py
```

3. Automating BigQuery Dashboards
Once data is in BigQuery, schedule SQL queries to refresh the dashboard in Google Data Studio or other BI tools.

## BigQuery Integration

Once uploaded, data can be queried directly in BigQuery:
```
SELECT * FROM `your_project.your_dataset.character_data`
LIMIT 10;
```
To visualize, connect BigQuery to Google Data Studio for interactive dashboards.

## notes

* Confidential Files: Ensure .gitignore prevents sensitive files (e.g., credentials) from being uploaded.
*BigQuery Costs: Be mindful of query and storage costs.

## Acknowledgments

* Google Cloud for storage and data processing.

* Hoyoverse (Hoyolab) for the original character data.

* Python libraries: requests, pandas, google-cloud-storage, etc.

## Future Improvements
* Implement parallelized scraping for improved efficiency.
* Develop a web dashboard for real-time monitoring.
* Expand support to other game platforms.

🚀 Happy scraping!






