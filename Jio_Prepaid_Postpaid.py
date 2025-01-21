import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_driver_path = r"C:\Users\DELL\PycharmProjects\Data_Scrapper_Project\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load data from Excel file
data = pd.read_csv('Indiamart_Result1.csv')

# Filter for rows where column B contains "Jio"
filtered_data = data[data['Operator'].str.contains("Jio", na=False, case=False)]

# Add empty columns for Status and Additional_Data if not already present
if "Status" not in data.columns:
    data["Status"] = ""


csv_file_path = r'C:\\Users\\DELL\\PycharmProjects\\Mobile_Number_Scraping\\Indiamart_Result3.csv'

# Open the website
def navigate_to_home():
    driver.get("https://www.jio.com/mobile")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[1]/div/span[2]/label/span/div"))).click()
    time.sleep(2)
navigate_to_home()

# Process each mobile number from the filtered data
for index, row in filtered_data.iterrows():
    number = row['Mobile Number']
    try:
        print(f"Processing number: {number}")

        # Input the mobile number
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[1]/div/input"))
        )
        input_field.clear()
        input_field.send_keys(str(number))
        print(f"Entered number: {number}")

        # Input the amount "1000"
        amount_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[1]/div[2]/div/input"))
        )
        driver.execute_script("arguments[0].focus(); arguments[0].value = '';", amount_field)
        amount_field.send_keys("1000")
        print("Entered amount: 1000")

        # Click the run button
        run_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/div/div[2]/button[1]/div"))
        )
        run_button.click()
        print("Clicked Run button")

        # Wait for results
        time.sleep(3)

        # Extract result message
        try:
            data_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='__next']/div/main/div/div[1]/section/div/div[2]/div[2]/div/div/div[2]/div/div/form/section/div/div/div/span"))
            ).text
            print(f"Response received for {number}: {data_element}")

            # Process result and update DataFrame
            if "prepaid" in data_element.lower():
                print(f"{number} is Prepaid")
                data.at[index, "Status"] = "Prepaid"
            elif "valid" in data_element.lower():
                print(f"{number} is Invalid")
                data.at[index, "Status"] = "N/A"
            else:
                raise Exception("Postpaid condition met")
        except Exception:
            # New tab opens for Postpaid handling
            print(f"Opening new tab for {number} as Postpaid condition met.")
            driver.execute_script("window.open('');")  # Open a new tab
            driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

            # Navigate to Postpaid page if required
            navigate_to_home()

            # Assume Postpaid status since we are in this block
            print(f"{number} identified as Postpaid. Updating status.")
            data.at[index, "Status"] = "Postpaid"

            # Close the new tab and return to the original tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # Switch back to original tab

        # Save the updated DataFrame incrementally
        data.to_csv(csv_file_path, index=False)

    except Exception as e:
        print(f"Error processing number {number}: {e}")

    finally:
        # Always navigate back to the home page for the next number
        navigate_to_home()

# Final save of the DataFrame
data.to_csv(csv_file_path, index=False)

# Close the browser
driver.quit()
print("Data scraping completed!")

