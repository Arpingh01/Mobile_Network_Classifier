# Mobile_Network_Classifier

## Overview
The **Mobile_Network_Classifier** is a Python-based project designed to classify mobile numbers by their network operator and plan type (prepaid or postpaid). 
The project consists of multiple scripts that scrape data from various sources, process it and generate consolidated results in CSV format.

## Project Structure

### 1. `Paytm_Operator_Circle.py`
- **Functionality:**
  - Scrapes the Paytm website to determine the operator and circle (region) of a given mobile number.
  - Saves the extracted data into a new CSV file.

### 2. `Jio_Prepaid_Postpaid.py`
- **Functionality:**
  - Checks whether a number belongs to Jio and identifies if it is prepaid or postpaid.

### 3. `Vi_Prepaid_Postpaid.py`
- **Functionality:**
  - Checks whether a number belongs to Vi and identifies if it is prepaid or postpaid.

### 4. `Airtel_Prepaid_Postpaid.py`
- **Functionality:**
  - Checks whether a number belongs to Airtel and identifies if it is prepaid or postpaid.

### 6. `Combinational_(AJV)_Prepaid_Postpaid.py`
- **Functionality:**
  - Combines the functionality of the individual network scripts (Jio, Vi, Airtel).
  - Processes each mobile number sequentially through the Jio, Vi, and Airtel scripts.
  - Classifies numbers into categories such as:
    - Jio Prepaid
    - Jio Postpaid
    - Vi Prepaid
    - Vi Postpaid
    - Airtel Prepaid
    - Airtel Postpaid
    - NA (Not Available/Not Found)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mobile-network-classifier.git
   cd mobile-network-classifier
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure the input CSV file is prepared with mobile numbers.

## Usage

1. **Run `Paytm_Operator_Circle.py` to scrape operator and circle information:**
   ```bash
   python script2_paytm.py
   ```

2. **Run individual scripts for network classification:**
   - For Jio:
     ```bash
     python Jio_Prepaid_Postpaid.py
     ```
   - For Vi:
     ```bash
     python Vi_Prepaid_Postpaid.py
     ```
   - For Airtel:
     ```bash
     python Airtel_Prepaid_Postpaid.py
     ```

3. **Run `Combinational_(AJV)_Prepaid_Postpaid.py` for complete classification:**
   ```bash
   python combinational_script.py
   ```

## Output
- The processed data is saved as a CSV file.
- Each script appends relevant data to the output file, ensuring a consolidated view.

## Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to create an issue or submit a pull request.


**Author:** [Arpita Singh]

