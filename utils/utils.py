import os
from pandas_gbq import read_gbq, to_gbq
import pandas as pd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET = os.getenv("DATASET")
TABLE_SOURCE = os.getenv("TABLE_SOURCE")

def fetch_data_from_bigquery() -> pd.DataFrame:
    """Use pandas_gbq to query data from Bigquery"""
    query = f"SELECT domain FROM `{PROJECT_ID}.{DATASET}.{TABLE_SOURCE}`"
    df = read_gbq(query, project_id=PROJECT_ID)
    return df



def send_to_bigquery(df: pd.DataFrame, table_name: str):
    """Use pandas_gbq to send dataframe to Bigquery"""
    destination = f"{PROJECT_ID}.{DATASET}.{table_name}"
    to_gbq(df, destination, project_id=PROJECT_ID, if_exists='replace')  # Adjust if_exists as needed


def safe_find_text(driver, xpath, default=""):
    """Finds an element and returns its text or a default value if not found."""
    try:
        return driver.find_element(By.XPATH, xpath).text
    except:
        return default

def safe_extract_text_from_object(elements, index1, index2, default=""):
    """Safely extracts text from a list of elements or returns a default value."""
    try:
        return elements[index1][index2]
    except IndexError:
        return default