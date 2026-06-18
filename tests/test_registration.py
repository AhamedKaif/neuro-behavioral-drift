from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import uuid

def test_valid_registration(browser):
    """Test registering a new user."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    # Ensure we are on registration mode
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
        
    browser.find_element(By.XPATH, "//input[@name='full_name']").send_keys("Test User")
    
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(unique_username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element(By.XPATH, "//input[@name='age']").send_keys("25")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='working_hours']").send_keys("8")
    browser.find_element(By.XPATH, "//input[@name='avg_screen_time']").send_keys("6")
    browser.find_element(By.XPATH, "//input[@name='avg_sleep_hours']").send_keys("7")
    
    checkbox = browser.find_element(By.XPATH, "//input[@name='privacy_consent']")
    browser.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    checkbox.click()
    
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()
    
    # Assert successful registration redirects to dashboard
    WebDriverWait(browser, 20).until(EC.url_contains("dashboard"))
    
    # Logout for next test
    browser.execute_script("window.localStorage.clear();")

def test_registration_existing_user(browser):
    """Test registering with an already existing username."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    # Create user first
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
        
    browser.find_element(By.XPATH, "//input[@name='full_name']").send_keys("Test User")
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(unique_username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element(By.XPATH, "//input[@name='age']").send_keys("25")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='working_hours']").send_keys("8")
    browser.find_element(By.XPATH, "//input[@name='avg_screen_time']").send_keys("6")
    browser.find_element(By.XPATH, "//input[@name='avg_sleep_hours']").send_keys("7")
    
    checkbox = browser.find_element(By.XPATH, "//input[@name='privacy_consent']")
    browser.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    checkbox.click()
    
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()
    
    # Wait for dashboard
    WebDriverWait(browser, 20).until(EC.url_contains("dashboard"))
    
    # Logout
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    # Try registering again
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
        
    browser.find_element(By.XPATH, "//input[@name='full_name']").send_keys("Test User")
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(unique_username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{unique_username}2@example.com") # different email
    browser.find_element(By.XPATH, "//input[@name='age']").send_keys("25")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='working_hours']").send_keys("8")
    browser.find_element(By.XPATH, "//input[@name='avg_screen_time']").send_keys("6")
    browser.find_element(By.XPATH, "//input[@name='avg_sleep_hours']").send_keys("7")
    
    checkbox = browser.find_element(By.XPATH, "//input[@name='privacy_consent']")
    browser.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    checkbox.click()
    
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()
    
    error_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-red-400')]")))
    assert "already exists" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_registration_empty_fields(browser):
    """Test submitting registration form with empty fields."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
        
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()
    
    # Should show error about filling fields
    error_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-red-400')]")))
    assert "fill in all" in error_msg.text.lower()
