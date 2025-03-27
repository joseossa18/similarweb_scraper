from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import safe_find_text, safe_extract_text_from_object
import time
import pandas as pd



# Function to scrape SimilarWeb and click a button
def scrape_similarweb(website: str, driver: webdriver.Chrome):
    #Initializing variables to handle errors in the scraping
    description = ""
    total_visits = ""
    visits_change = ""
    device_distribution_dict = ""
    global_rank = ""
    country = ""
    country_rank = ""
    industry = ""
    industry_rank = ""
    monthly_visits = ""
    monthly_unique_visitors = ""
    deduplicated_audience = ""
    visit_duration = ""
    pages_per_visit = ""
    bounce_rate = ""
    source_of_traffic_dict = ""
    similar_web_dict = ""

    driver.get(f"https://pro.similarweb.com/#/activation/home/")

    try:
        # Wait for the button to be clickable (you can use WebDriverWait for better practice)
        button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@class="sc-hqyNC sc-gGBfsJ fWSpQE Button sc-esjQYD sc-ibxdXY ekcrNr"]'))
)
        
        # Click the button
        button.click()
        print(f"Clicked the button on {website}")

        # Wait for any content to load after clicking
        time.sleep(2)

    except Exception as e:
        print(f"Failed to click on configurations for {website}: {str(e)}")

    try:
        #removing old website from the input
        company_name_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="sc-BngTV sc-jUpvKA jckYwz fake-input--content"]'))
        )
        company_name_div.click()
    except Exception as e:
        print(f"Failed to remove old website name for {website}: {str(e)}")

    try:
        #adding the new website in the input
        company_name_text = driver.find_element(By.XPATH, '//div[starts-with(@class, "sc-jtRlXQ Mimor AutocompleteStyled")]//input')
        company_name_text.send_keys(website)
        time.sleep(1)

    except Exception as e:
        print(f"Failed to write new website name for {website}: {str(e)}")

    try:
        #Click on the input so that the new name stays
        company_name_select = driver.find_element(By.XPATH, '//div[@class="sc-kjoXOD iiqbAx ItemText"]')
        company_name_select.click()
        time.sleep(1)

    except Exception as e:
        print(f"Failed to click on the website name so it can be saved for {website}: {str(e)}")

    try:
        #Click on save changes button
        save_changes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="sc-hqyNC sc-uJMKN flxlYJ Button"]'))
        )
        driver.execute_script("arguments[0].click();", save_changes_button)
        time.sleep(2)

    except Exception as e:
        print(f"Failed to click on save changes button for {website}: {str(e)}")


    try:
        #go to performance pag
        driver.get(f"https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/3m?webSource=Total&key={website}")
    except Exception as e:
        print(f"Failed to go to performance page for {website}: {str(e)}")

    try:
        # Locate the parent div
        parent_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@class, "BaseFlex-bGFvgJ FlexRow-dhmstB TopPageWidgetsRow")]'))  # Change class name
        )
        #Traffic & Engagement
        description = safe_find_text(driver, './/div[starts-with(@class, "DescriptionText-")]', default="")
        total_visits = safe_find_text(parent_div, './/div[starts-with(@class, "TotalNumberStyled-")]', default="")
        visits_change = safe_find_text(parent_div, './/span[@class="ChangeValue-text ChangeValue-text--symbol"]', default="")
        print(description)

        try:
            device_distribution_child = parent_div.find_elements(By.XPATH, './/div[@class="highcharts-legend highcharts-no-tooltip"]')
            for parent in device_distribution_child:
                children = parent.find_elements(By.XPATH, './/div[@class="BaseFlex-bGFvgJ FlexRow-dhmstB gUmaNS"]')  # Finds only direct child divs
                device_distribution_text = [child.text.strip() for child in children]
            try:
                device_distribution_dict = {
                            'desktop': device_distribution_text[0].split('\n')[1].strip('%'),
                            'mobile_web': device_distribution_text[1].split('\n')[1].strip('%')
                }
            except:
                device_distribution_dict = ""
        except: 
            device_distribution_text = ""

        try:
            ranking_child = parent_div.find_elements(By.XPATH, './/div[starts-with(@class, "BaseFlex-bGFvgJ FlexRow-dhmstB RankDataRow-")]')

            ranking_text = []
            for parent in ranking_child:
                children = parent.find_elements(By.XPATH, './/div[starts-with(@class, "TextStyled-") or starts-with(@class, "RankNumberStyled-")] | .//a[ starts-with(@class, "sc-jMvuUo ciAuvE StyledLink-")]')  # Finds only direct child divs
                row = [child.text.strip() for child in children]  # Remove empty texts
                if row:  # Ensure there's data before appending
                    ranking_text.append(row)
        except: 
            ranking_text = ""

        global_rank = safe_extract_text_from_object(ranking_text, 0, 1)
        country = safe_extract_text_from_object(ranking_text, 1, 1)
        country_rank = safe_extract_text_from_object(ranking_text, 1, 2)
        industry = safe_extract_text_from_object(ranking_text, 2, 1)
        industry_rank = safe_extract_text_from_object(ranking_text, 2, 2)

    except Exception as e:
        print(f"Failed to extract performance data for {website}: {str(e)}")

    try:
         #Engagement overview
        # Locate the parent div
        parent_div = driver.find_element(By.XPATH, '//div[starts-with(@class, "MetricsContainer-")]')  # Change class name

        engagement_overview_child = parent_div.find_elements(By.XPATH, './/div[starts-with(@class, "MetricContainer-")]')

        engagement_overview_text = []
        for parent in engagement_overview_child:
            children = parent.find_elements(By.XPATH, './/div[starts-with(@class, "MetricName-") or starts-with(@class, "MetricValue-")]')  # Finds only direct child divs
            if len(children) >= 2:  # Ensure at least 2 divs exist
                engagement_overview_text.append([children[0].text.strip(), children[1].text.strip()])

        monthly_visits = safe_extract_text_from_object(engagement_overview_text, 0, 1)
        monthly_unique_visitors = safe_extract_text_from_object(engagement_overview_text, 1, 1)
        deduplicated_audience = safe_extract_text_from_object(engagement_overview_text, 2, 1)
        visit_duration = safe_extract_text_from_object(engagement_overview_text, 3, 1)
        pages_per_visit = safe_extract_text_from_object(engagement_overview_text, 4, 1)
        bounce_rate = safe_extract_text_from_object(engagement_overview_text, 5, 1)

    except Exception as e:
        print(f"Failed to extract engagement overview data for {website}: {str(e)}")



    try:
         #Source of Traffic
        parent_div = driver.find_element(By.XPATH, '//div[starts-with(@class, "ChannelsOverviewBarChartWrapper-")]')  # Change class name

        try:
            source_traffic_names_child = parent_div.find_element(By.XPATH, './/div[@class="highcharts-axis-labels highcharts-xaxis-labels"]')
            children = source_traffic_names_child.find_elements(By.XPATH, './/span')  # Finds only direct child divs
            source_traffic_names = [child.text.strip() for child in children]  # Remove empty texts
        except: 
            source_traffic_names = ""

        try:
            source_traffic_values_child = parent_div.find_element(By.XPATH, './/div[@class="highcharts-stack-labels"]')
            children = source_traffic_values_child.find_elements(By.XPATH, './/span')  # Finds only direct child divs
            source_traffic_values = [child.text.strip() for child in children]  # Remove empty texts
        except:
            source_traffic_values=""
        source_traffic = list(zip(source_traffic_names, source_traffic_values))

        try:
            source_of_traffic_dict = {item[0]: item[1] for item in source_traffic}
        except:
            source_of_traffic_dict = ""
    except Exception as e:
        print(f"Failed to extract source traffic for {website}: {str(e)}")

    try:
        # Go to Similar sites page
        driver.get(f"https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/competitive-landscape/*/999/3m?key={website}")
        wait = WebDriverWait(driver, 10)

        try:
            similar_web_name = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[(@class="swReactTableCell swTable-cell resizeableCell-hover even" or @class="swReactTableCell swTable-cell resizeableCell-hover even active-row" or @class="swReactTableCell swTable-cell resizeableCell-hover odd") and @data-table-col="2"][position() <= 5]')))
            similar_web_name_text = []
            for parent in similar_web_name:
                child_div = parent.find_element(By.XPATH, './/div[@class="swTable-content-large text"]//a').text
                similar_web_name_text.append(child_div)
        except:
            similar_web_name_text = ""
        
        try:
            similar_web_industry = driver.find_elements(By.XPATH, './/div[(@class="swReactTableCell swTable-cell resizeableCell-hover even" or @class="swReactTableCell swTable-cell resizeableCell-hover even active-row" or @class="swReactTableCell swTable-cell resizeableCell-hover odd") and @data-table-col="3"][position() <= 5]')
            similar_web_industry_text = [child.text.strip() for child in similar_web_industry]
        except:
            similar_web_industry_text =""
        try:
            similar_web_rank = driver.find_elements(By.XPATH, './/div[(@class="swReactTableCell swTable-cell resizeableCell-hover even" or @class="swReactTableCell swTable-cell resizeableCell-hover even active-row" or @class="swReactTableCell swTable-cell resizeableCell-hover odd") and @data-table-col="4"][position() <= 5]')
            similar_web_rank_text = [child.text.strip() for child in similar_web_rank]
        except:
            similar_web_rank_text =""
        try:
            similar_web_affinity = driver.find_elements(By.XPATH, './/div[(@class="swReactTableCell swTable-cell resizeableCell-hover even" or @class="swReactTableCell swTable-cell resizeableCell-hover even active-row" or @class="swReactTableCell swTable-cell resizeableCell-hover odd") and @data-table-col="5"][position() <= 5]')
            similar_web_affinity_text = [child.text.strip() for child in similar_web_affinity]
        except:
            similar_web_affinity_text =""

        similar_web = list(zip(similar_web_name_text, similar_web_industry_text, similar_web_rank_text, similar_web_affinity_text))

        try:
            similar_web_dict = {
                'website': [item[0] for item in similar_web],
                'industry': [item[1] for item in similar_web],
                'ranking': [item[2] for item in similar_web],
                'affinity': [item[3] for item in similar_web]
            }
        except:
            similar_web_dict = ""
    except Exception as e:
        print(f"Failed to extract similar websites for {website}: {str(e)}")

#Create a dictionary with all the collected data
    website_data = {
        "website": website,
        "description":description,
        "total_visits": total_visits,
        "visits_change_last_month": visits_change,
        "device_distribution": device_distribution_dict,
        "global_rank": global_rank,
        "country": country,
        "country_rank": country_rank,
        "industry": industry,
        "industry_rank": industry_rank,
        "monthly_visits":monthly_visits,
        "monthly_unique_visitors":monthly_unique_visitors,
        "deduplicated_audience":deduplicated_audience,
        "visit_duration":visit_duration,
        "pages_per_visit":pages_per_visit,
        "bounce_rate":bounce_rate,
        "source_of_traffic": source_of_traffic_dict,
        "similar_websites": similar_web_dict
    }

    return website_data
