import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options and driver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_driver_path = r"C:\\Users\\DELL\\PycharmProjects\\Data_Scrapper_Project\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load data
csv_file_path = r"C:\\Users\\DELL\\PycharmProjects\\Mobile_Number_Scraping\\Indiamart_Result3.csv"
data = pd.read_csv(csv_file_path)

# Filter data for rows containing "Airtel" in column 'B'
filtered_data = data[data['Operator'].str.contains("Airtel", na=False, case=False)]

# Add "Status" column if it doesn't exist
if "Status" not in data.columns:
    data["Status"] = ""

# Navigate to Airtel website
def navigate_to_home():
   driver.get("https://www.airtel.in/")
   time.sleep(2)
navigate_to_home()
for index, row in filtered_data.iterrows():
    number = row['Mobile Number']
    try:
        # Interact with the input field
        input_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div/div[3]/div/div/div/input"))
        )
        input_field.clear()
        input_field.send_keys(str(number))
        time.sleep(5)

        # Check prepaid status
        try:
            response_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/h6"))
            )
            response_text = response_element.text.strip().lower()
            print(f"Response for {number}: {response_text}")
            data.at[index, "Status"] = "Prepaid"

        except Exception:
            # Navigate to postpaid page if not prepaid
            driver.get("https://www.airtel.in/postpaid-bill-pay?icid=header")
            postpaid_input = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,"/html/body/main/div/div[2]/div[1]/form/div[1]/input"))
            )
            postpaid_input.clear()
            postpaid_input.send_keys(str(number))
            time.sleep(5)

            try:
                postpaid_response = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[1]/form/div[1]"))
                )
                response_text = postpaid_response.text.strip().lower()
                print(f"Response for {number}: {response_text}")
                data.at[index, "Status"] = "Postpaid"
            except Exception:
                data.at[index, "Status"] = "N/A"

    except Exception as e:
        print(f"Error processing number {number}: {e}")
        data.at[index, "Status"] = "Error"

    # Save progress after processing each number
    print(f"Saving data after processing number {number}")
    data.to_csv(csv_file_path, index=False)
    navigate_to_home()

# Close the browser
driver.quit()
print("Data scraping completed!")



