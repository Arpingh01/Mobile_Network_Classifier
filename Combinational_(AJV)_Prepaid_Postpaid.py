#import library
import os
import csv
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_driver_path = r"C:\Users\DELL\PycharmProjects\Data_Scrapper_Project\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load data
input_csv = r"C:\Users\DELL\PycharmProjects\Mobile_Number_Scraping\Indiamart_Data.csv"
output_csv = r"C:\Users\DELL\PycharmProjects\Mobile_Number_Scraping\Indiamart_Result.csv"

# Read data
data = pd.read_csv(input_csv)
mobile_numbers = data['mobileNumber1']

# Make Column Name"
mobile_numbers = data['mobileNumber1']
if not os.path.exists(output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Mobile Number', 'Status', 'Date', 'Time'])

# Navigate to the Jio website
def navigate_to_home():
   print("Opening Jio Website")
   driver.get("https://www.jio.com/mobile")
   time.sleep(2)
navigate_to_home()

for index, number in enumerate(mobile_numbers):
    try:
        print(f"Processing number: {number}")
        current_datetime = datetime.now()
        Date = current_datetime.strftime('%Y-%m-%d')
        Time = current_datetime.strftime('%H:%M:%S')
        status = "Unknown"

        # Input the mobile number on Jio
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[1]/div/input"))
        )
        input_field.clear()
        input_field.send_keys(str(number))

        run_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/button/div"))
        )
        run_button.click()
        time.sleep(5)

        # Fetch response
        try:
            data_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[2]/section/section/section/section[1]/div/div[1]/div/div/div/span[2]/span"))
            ).text.strip().lower()
            time.sleep(5)
        except Exception:
            data_element = ""
        if "recharging for" in data_element:
            print(f"{number} is Prepaid")
            Status = "Jio Prepaid"
            print(f"Saving data of {number}:Jio Prepaid")
        elif "get add-on for" in data_element:
            print(f"{number} is Postpaid")
            Status = "Jio Postpaid"
            print(f"Saving data of {number}:Jio Postpaid")
        else:
             print("It is not a Jio number")
             # Navigate to Airtel website
             print("Opening Airtel Website")
             driver.get("https://www.airtel.in/")
             time.sleep(2)
             input_field = WebDriverWait(driver, 5).until(
                  EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div/div[3]/div/div/div/input"))
                  )
             input_field.clear()
             input_field.send_keys(str(number))
             time.sleep(5)
             print(f"Processing number: {number}")
             try:
                 response_element = WebDriverWait(driver, 5).until(
                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/h6"))
                  )
                 response_text = response_element.text.strip().lower()
                 print(f"Response for {number}: {response_text}")
                 Status = "Airtel Prepaid"
                 print(f"Saving data of {number}:Airtel Prepaid")

             except Exception:
                       print(f"{number} is not a airtel prepaid number.")
                       # Navigate to postpaid page if not prepaid
                       driver.get("https://www.airtel.in/postpaid-bill-pay?icid=header")
                       postpaid_input = WebDriverWait(driver, 5).until(
                       EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[2]/div[1]/form/div[1]/input"))
                       )
                       postpaid_input.clear()
                       postpaid_input.send_keys(str(number))
                       time.sleep(5)

                       try:
                           postpaid_response = WebDriverWait(driver, 5).until(
                           EC.visibility_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[1]/form/div[1]"))
                           )
                           postpaid_text = postpaid_response.text.strip().lower()
                           postpaid_text1 = WebDriverWait(driver, 5).until(
                           EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[2]/div[1]/form/div[2]/input")))
                           postpaid_text1.clear()
                           postpaid_text1.send_keys(1000)
                           time.sleep(2)
                           print(f"Response for {number}: {postpaid_text}")
                           Status= "Airtel Postpaid"
                           print(f"Saving data of {number}:Airtel Postpaid")

                       except Exception:
                             print(f"{number} is not a airtel postpaid number.")
                             print("Opening Vi Website")
                             driver.get("https://www.myvi.in/postpaid/quick-online-bill-payment")
                             time.sleep(2)
                             try:
                                 input_field = WebDriverWait(driver, 10).until(
                                 EC.element_to_be_clickable(
                                 (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/section/div/div/div[2]/div[1]/div/div/div[2]/div[1]/input"))
                                  )
                                 input_field.clear()
                                 input_field.send_keys(str(number))
                                 time.sleep(5)
                                 try:
                                     response_element = WebDriverWait(driver, 10).until(
                                     EC.visibility_of_element_located(
                                    (By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/section/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div[2]"))
                                     )
                                     data_element = response_element.text.strip().lower()
                                     print(f"Response received for {number}: {data_element}")
                                     time.sleep(5)
                                     # Determine the status based on the response text
                                     if "This number is not an active Vi User." in data_element:
                                         Status = "N/A"
                                         print(f"Saving data of {number}:N/A")
                                     elif "This seems to be a prepaid number." in data_element:
                                         Status = "Vi Prepaid"
                                         print(f"Saving data of {number}:Vi Prepaid")

                                     else:
                                         raise Exception("Postpaid condition met")
                                 except Exception :
                                        Status = "Vi Postpaid"
                                        print(f"Saving data of {number}:Vi Postpaid")

                             except Exception as e :
                                 print(f"Error processing number {number}: {e}")
                                 Status = "Error"

    except Exception as e:
          print(f"Error processing number {number}: {e}")
          Status = "Error"
    with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([number, Status, Date, Time])
    navigate_to_home()

driver.quit()
print("Data scraping completed!")