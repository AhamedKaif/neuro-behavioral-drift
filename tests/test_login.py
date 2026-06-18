from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import uuid

def setup_user(browser):
    """Helper to create a user for login tests."""
    username = f"login_test_{uuid.uuid4().hex[:6]}"
    password = "password123"
    
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    # Refresh to ensure we are logged out
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))
        
    browser.find_element(By.XPATH, "//input[@name='full_name']").send_keys("Test User")
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{username}@example.com")
    browser.find_element(By.XPATH, "//input[@name='age']").send_keys("25")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys(password)
    browser.find_element(By.XPATH, "//input[@name='working_hours']").send_keys("8")
    browser.find_element(By.XPATH, "//input[@name='avg_screen_time']").send_keys("6")
    browser.find_element(By.XPATH, "//input[@name='avg_sleep_hours']").send_keys("7")
    
    checkbox = browser.find_element(By.XPATH, "//input[@name='privacy_consent']")
    browser.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    checkbox.click()
    
    submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()
    
    WebDriverWait(browser, 20).until(EC.url_contains("dashboard"))
    
    # Logout
    browser.execute_script("window.localStorage.clear();")
    return username, password

def test_valid_login(browser):
    """Test logging in with valid credentials."""
    username, password = setup_user(browser)
    
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    # Ensure login mode
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']")))
        
    browser.find_element(By.XPATH, "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element(By.XPATH, "//input[@placeholder='Enter password']").send_keys(password)
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    WebDriverWait(browser, 20).until(EC.url_contains("dashboard"))
    browser.execute_script("window.localStorage.clear();")

def test_invalid_password(browser):
    """Test logging in with an invalid password."""
    username, _ = setup_user(browser)
    
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']")))
        
    browser.find_element(By.XPATH, "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element(By.XPATH, "//input[@placeholder='Enter password']").send_keys("wrongpassword")
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    
    error_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-red-400')]")))
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_invalid_username(browser):
    """Test logging in with a non-existent username."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']")))
        
    browser.find_element(By.XPATH, "//input[@placeholder='Enter username']").send_keys(f"nonexistent_{uuid.uuid4().hex[:6]}")
    browser.find_element(By.XPATH, "//input[@placeholder='Enter password']").send_keys("password")
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    
    error_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-red-400')]")))
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_login_empty_fields(browser):
    """Test logging in with empty fields."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/")
    
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    
    toggles = browser.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']")))
        
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    
    error_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-red-400')]")))
    assert "fill in all fields" in error_msg.text.lower()
