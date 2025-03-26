from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Function to set up the Chrome WebDriver with a custom profile
def setup_driver(profile_path: str, profile: str):
    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument(f"profile-directory={profile}")
    #options.add_argument("--headless")  # Run headless (without GUI)
    driver_path = "chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver