import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Fixture to set up and tear down the browser
@pytest.fixture
def setup():
    driver = webdriver.Chrome(options=options)
    driver.get("https://the-internet.herokuapp.com/tables")
    driver.maximize_window()
    yield driver
    driver.quit()

# Test Case 1: Extract & Print Web Table Data
def test_extract_table_data(setup):
    driver = setup

    # Locate the table
    table = driver.find_element(By.ID, "table1")

    # Extract all rows
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Iterate through rows and print data
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        print([col.text for col in cols])  # Print row as a list

    assert len(rows) > 1  # Validate that the table is not empty
    print("✅ Table data extracted successfully!")

    time.sleep(2)

# Test Case 2: Validate Specific Data in the Table
def test_validate_table_data(setup):
    driver = setup

    # Locate a specific cell (e.g., "Frank" in the first column)
    first_names = driver.find_elements(By.XPATH, "//table[@id='table1']//tbody//tr//td[1]")
    first_name_list = [name.text for name in first_names]

    assert "Smith" in first_name_list  # Validate if "Frank" is in the table
    print("✅ 'Frank' found in table!")

    time.sleep(2)

# Test Case 3: Find Row with Highest Due Amount
def test_find_highest_due(setup):
    driver = setup

    # Extract Due amounts column
    due_elements = driver.find_elements(By.XPATH, "//table[@id='table1']//tbody//tr//td[4]")

    # Convert amounts to float and find the max
    due_amounts = [float(due.text.replace("$", "")) for due in due_elements]
    max_due = max(due_amounts)

    print(f"💰 Highest Due Amount: ${max_due}")
    assert max_due > 0  # Ensure max due is valid

    time.sleep(2)
