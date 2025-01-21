import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv

# Path to your chromedriver.exe file
driver_path =  "C:\\Users\\DELL\\PycharmProjects\\Data_Scrapper_Project\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"

# Check if the driver path is valid
if not os.path.isfile(driver_path):
    raise FileNotFoundError(f"ChromeDriver not found at {driver_path}. Please verify the path.")

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")

# Set up the Service object
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Read mobile numbers from the Client Number column in the CSV file
df = pd.read_csv("Indiamart_Data.csv")

# Verify column names and make sure 'Client Number' exists
print(df.columns)

# Extract the first 20 mobile numbers from the 'Client Number' column
mobile_numbers = df['mobileNumber1']

# Path for the output CSV file
csv_file_path = r'C:\Users\DELL\PycharmProjects\Mobile_Number_Scraping\Indiamart_Result1.csv'

# Create the CSV file and write headers if the file doesn't exist
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Mobile Number', 'Operator', 'Circle', 'Date', 'Time'])  # Write headers

# Iterate over each mobile number
for mobile_number in mobile_numbers:
    print(f"Processing {mobile_number}...")  # Debugging statement

    # Open Paytm recharge page
    driver.get('https://paytm.com/recharge')
    time.sleep(2)  # Ensure the page loads completely before proceeding

    try:
        # Wait for the Mobile Number input field to be present
        mobile_number_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[4]/div[1]/div/div/div[2]/div[2]/ul/li[1]/div[1]/div/input"))
        )
        mobile_number_input.clear()
        mobile_number_input.send_keys(str(mobile_number))
        mobile_number_input.send_keys(Keys.RETURN)

        # Wait for operator and circle details to load
        time.sleep(5)  # Ensure Paytm has time to process the number and load the data

        operator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[4]/div[1]/div[1]/div/div/div[2]/ul/li[2]/div[1]/div/input"))
        ).get_attribute('value') or 'N/A'

        circle = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[4]/div[1]/div[1]/div/div/div[2]/ul/li[3]/div[1]/div/input"))
        ).get_attribute('value') or 'N/A'

        print(f"Operator: {operator}, Circle: {circle}")

    except Exception as e:
        print(f"Error extracting data for {mobile_number}: {e}")
        operator = 'N/A'
        circle = 'N/A'

    # Get the current date and time
    current_datetime = datetime.now()
    scraping_date = current_datetime.strftime('%Y-%m-%d')  # Extract date
    scraping_time = current_datetime.strftime('%H:%M:%S')  # Extract time

    # Append the data to the CSV file
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([mobile_number, operator, circle, scraping_date, scraping_time])  # Append data

    # Add a delay before processing the next number
    time.sleep(5)  # Prevent overloading the page by adding a delay

# Close the browser
driver.quit()

print("Data scraping completed!")

