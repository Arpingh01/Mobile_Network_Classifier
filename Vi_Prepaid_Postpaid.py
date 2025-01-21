import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options and driver path
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_driver_path = r"C:\Users\DELL\PycharmProjects\Data_Scrapper_Project\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read data
csv_file_path = r"C:\Users\DELL\PycharmProjects\Mobile_Number_Scraping\Indiamart_Result3.csv"
data = pd.read_csv(csv_file_path)

# Filter data for rows containing "Vi" in column 'B'
filtered_data = data[data['Operator'].str.contains("Vi", na=False, case=False)]

# Add "Status" column if it doesn't exist
if "Status" not in data.columns:
    data["Status"] = ""

# Navigate to the website

driver.get("https://www.myvi.in/prepaid/online-mobile-recharge")
time.sleep(2)


# Process each number
for _, row in filtered_data.iterrows():
    number = row['Mobile Number']
    try:
        print(f"Processing number: {number}")

        # Locate and input the number
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div[1]/div/section/div/div[1]/div[2]/input"))
        )
        input_field.clear()
        input_field.send_keys(str(number))
        time.sleep(5)

        # Extract the response
        try:
            response_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[3]/div/div[3]/div[1]/div/section/div/div[1]/div[2]/div[2]"))
            )
            data_element = response_element.text.strip().lower()
            print(f"Response received for {number}: {data_element}")
            time.sleep(5)
            # Determine the status based on the response text
            if "non vi number" in data_element:
                data.loc[row.name, "Status"] = "N/A"
            elif "postpaid number" in data_element:
                data.loc[row.name, "Status"] = "Postpaid"
            else:
                raise Exception("Prepaid condition met")
        except Exception :
            print(f"{number} identified as Prepaid. Updating status.")
            data.loc[row.name, "Status"] = "Prepaid"
            data.to_csv(csv_file_path, index=False)
    except Exception as e:
        print(f"Error processing number {number}: {e}")
        data.loc[row.name, "Status"] = "Error"


    # Save the updated data to CSV after processing each number
    print(f"Saving data after processing number {number}...")
    data.to_csv(csv_file_path, index=False)


# Close the browser
driver.quit()
print("Data scraping completed!")