# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
from selenium.webdriver.chrome.service import Service

# # Path to your webdriver
# service = Service()
# options = webdriver.ChromeOptions()

# # URL of the webpage
# url = 'https://moodle.hochschule-heidelberg.de/auth/oauth2/login.php?id=1&wantsurl=%2F&sesskey=pa2LjApYh9'

# # Initialize the WebDriver
# driver = webdriver.Chrome(service=service, options=options)

# # Open the webpage
# driver.get(url)

# # Wait for the page to load
# time.sleep(2)  # Adjust the sleep time as necessary

# # Find and click the login button
# try:
#     login_button = driver.find_element(By.CLASS_NAME, "btn-outline-light")
#     login_button.click()
#     print("Access!!!")
#     # Add any additional steps here (like filling the login form)
#     # ...

# except Exception as e:
#     print("Error:", e)

# # Close the browser when done (or keep it open if you need to do more interactions)
# # driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

service = Service()
options = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Function to log in (modify this according to the actual login process)
def login(driver):
    url = 'https://moodle.hochschule-heidelberg.de/auth/oauth2/login.php?id=1&wantsurl=%2F&sesskey=pa2LjApYh9'
    driver.get(url)
    time.sleep(2)  # Adjust the sleep time as necessary
    try:
        login_button = driver.find_element(By.CLASS_NAME, "alternate-login")
        login_button.click()
        print("Success!!!")

    except Exception as e:
        print("Error:", e)
    pass

# Log in to the website
login(driver)
time.sleep(60)
# Navigate to the specific page
driver.get("https://moodle.hochschule-heidelberg.de/course/view.php?id=4615&section=1#tabs-tree-start")
time.sleep(5)  # Wait for the page to load completely

# Find all div tags with class 'activityname'
activity_divs = driver.find_elements(By.CLASS_NAME, "activityname")

# Extract links from 'a' tags within these divs
activity_links = [div.find_element(By.TAG_NAME, "a").get_attribute('href') for div in activity_divs]

# Setup a directory for downloads
download_dir = "/Users/nguyentienhuy/Documents/SRH/CaseStudy/Data"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configure Selenium to download files to the specified directory
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Download PDF from a given page
def download_pdf(driver, url):
    driver.get(url)
    time.sleep(3)
    try:
        pdf_link = driver.find_element(By.TAG_NAME, "a").get_attribute('href')
        if pdf_link.endswith(".pdf"):
            driver.get(pdf_link)
            time.sleep(1)
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")

# Visit each link and download the PDF
for link in activity_links:
    download_pdf(driver, link)
driver.quit()
