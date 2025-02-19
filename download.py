import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_data():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # You might need to specify the path to the chromedriver
    driver.get("https://doge.gov/savings")

    # Click "see more" in the Contracts table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[text()='Contracts']/following-sibling::div//table//td[contains(text(), 'see more')]"))
    ).click()

    # Click "see more" in the Real Estate table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[text()='Real Estate']/following-sibling::div//table//td[contains(text(), 'see more')]"))
    ).click()

    # Wait for the Contracts table to load and extract it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[text()='Contracts']/following-sibling::div//table"))
    )
    contracts_table = driver.find_element(By.XPATH, "//h2[text()='Contracts']/following-sibling::div//table")
    contracts_data_total_value = extract_table_data(contracts_table)

    # Wait for the Real Estate table to load and extract it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[text()='Real Estate']/following-sibling::div//table"))
    )
    real_estate_table = driver.find_element(By.XPATH, "//h2[text()='Real Estate']/following-sibling::div//table")
    real_estate_data_total_value = extract_table_data(real_estate_table)

    # Click the "Savings" element
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Total Contract Value']/following-sibling::span[text()='Savings']"))
    ).click()

    # Extract the Contracts data again
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[text()='Contracts']/following-sibling::div//table"))
    )
    contracts_data_savings = extract_table_data(contracts_table)

    # Extract the Real Estate data again
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[text()='Real Estate']/following-sibling::div//table"))
    )
    real_estate_table = driver.find_element(By.XPATH, "//h2[text()='Real Estate']/following-sibling::div//table")
    real_estate_data_savings = extract_table_data(real_estate_table)

    contracts_data = contracts_data_total_value.copy()
    contracts_data["Savings"] = contracts_data_savings.iloc[:, -1].values

    real_estate_data = real_estate_data_total_value.copy()
    real_estate_data["Savings"] = real_estate_data_savings.iloc[:, -1].values

    # Save to CSV
    contracts_data.to_csv('contracts.csv', index=False)
    real_estate_data.to_csv('real_estate.csv', index=False)

    # Close the driver
    driver.quit()

def extract_table_data(table_element):
    # Get the HTML content of the table
    table_html = table_element.get_attribute('outerHTML')
    
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(table_html, 'html.parser')
    
    # Extract the table headers
    headers = [th.get_text(strip=True) for th in soup.find_all('th')]
    
    # Extract the table rows
    rows = []
    for tr in soup.find_all('tr'):
        cells = tr.find_all('td')
        if not cells:
            continue
        row = []
        for i, cell in enumerate(cells):
            # Check if the current column is the "Link" column
            if headers[i] == "Link":
                # Extract the URL from the "title" attribute
                link = cell.get('title', '')
                row.append(link)
            else:
                row.append(cell.get_text(strip=True))
        rows.append(row)
    
    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    return df

if __name__ == "__main__":
    scrape_data()
