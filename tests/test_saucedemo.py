import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Fixture to set up and tear down the browser
@pytest.fixture
def setup():
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

# Test Case 1: Successful Login
def test_successful_login(setup):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Validate successful login
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    print("✅ Login successful")

# Test Case 2: Invalid Login (Wrong Password)
def test_invalid_login(setup):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    
    # Validate error message
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    assert "Username and password do not match" in error_message
    print("✅ Error message validated")

# Test Case 3: Add Product to Cart
def test_add_product_to_cart(setup):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Add first product to cart
    first_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()

    # Click on the cart icon
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Validate product in cart
    cart_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert first_product_name == cart_product_name
    print("✅ Product added to cart successfully")

# Test Case 4: Work with Dropdown (Sorting Products)
def test_sort_products(setup):
    from selenium.webdriver.support.ui import Select  # Import Select for dropdown handling
    
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Locate dropdown and sort by price (low to high)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    dropdown.select_by_value("lohi")

    # Get prices after sorting
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    price_values = [float(price.text.replace("$", "")) for price in prices]

    # Validate sorting order
    assert price_values == sorted(price_values)
    print("✅ Products sorted by price successfully")

