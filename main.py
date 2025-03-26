import os
from scraper.driver_setup import setup_driver
from scraper.scraper import scrape_similarweb
import time
import pandas as pd
import logging
from utils.utils import fetch_data_from_bigquery, send_to_bigquery
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Main function
def main():
    # Set up the Chrome WebDriver
    PROFILE_PATH = os.getenv("PROFILE_PATH")
    PROFILE = os.getenv("PROFILE") #using a specific profile so the session is stored and there is no need to login
    driver = setup_driver(PROFILE_PATH, PROFILE)

    df = fetch_data_from_bigquery() #Get the websites from the bigquery table
    list_websites = df["domain"].to_list()

    batch_size = 100  # Process batches of 100 websites
    num_batches = (len(list_websites) // batch_size) + (1 if len(list_websites) % batch_size > 0 else 0)

    run_number = 1
    for batch_num in range(num_batches):
        batch_websites = list_websites[batch_num * batch_size : (batch_num + 1) * batch_size]
        websites_data_df = pd.DataFrame(columns=["website", "description", "total_visits", "visits_change_last_month", "device_distribution", "global_rank",
                                                  "country", "country_rank", "industry", "industry_rank", "monthly_visits", "monthly_unique_visitors", 
                                                  "deduplicated_audience", "visit_duration", "pages_per_visit", "bounce_rate", "source_of_traffic", "similar_websites"])
        try:
            for website in batch_websites:
                print(f"Opening SimilarWeb for {website}... Iteration {run_number}")
                website_data = scrape_similarweb(website, driver) #Do the scraping of the specific website
                websites_data_df = pd.concat([websites_data_df, pd.DataFrame([website_data])], ignore_index=True)

                time.sleep(1)
                run_number = run_number + 1

            batch_filename = f"scraped_data_test_{batch_num + 1}"
            #websites_data_df.to_csv(batch_filename, index=False)
            send_to_bigquery(websites_data_df, batch_filename) #Send the data to bigquery once the batch is finished
        except Exception as e:
            print(f"Failed on batch {batch_num + 1}: {str(e)}")
    # Close the driver after the task is complete
    driver.quit()

    
if __name__ == "__main__":
    main()