from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

def setup_user(browser):
    """Helper to create a user for login tests."""
    username = f"login_test_{uuid.uuid4().hex[:6]}"
    password = "password123"
    
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@name='full_name']").send_keys("Test User")
    browser.find_element("xpath", "//input[@name='username']").send_keys(username)
    browser.find_element("xpath", "//input[@name='email']").send_keys(f"{username}@example.com")
    browser.find_element("xpath", "//input[@name='password']").send_keys(password)
    browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys(password)
    browser.find_element("xpath", "//input[@name='privacy_consent']").click()
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(2)
    
    # Logout
    browser.execute_script("window.localStorage.clear();")
    return username, password

def test_valid_login(browser):
    """Test logging in with valid credentials."""
    username, password = setup_user(browser)
    
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Ensure login mode
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys(password)
    browser.find_element("xpath", "//button[@type='submit']").click()
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    browser.execute_script("window.localStorage.clear();")

def test_invalid_password(browser):
    """Test logging in with an invalid password."""
    username, _ = setup_user(browser)
    
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys("wrongpassword")
    browser.find_element("xpath", "//button[@type='submit']").click()
    WebDriverWait(browser, 10).until(EC.url_contains("login"))
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_invalid_username(browser):
    """Test logging in with a non-existent username."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(f"nonexistent_{uuid.uuid4().hex[:6]}")
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys("password")
    browser.find_element("xpath", "//button[@type='submit']").click()
    WebDriverWait(browser, 10).until(EC.url_contains("login"))
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_login_empty_fields(browser):
    """Test logging in with empty fields."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(1)
    
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "fill in all fields" in error_msg.text.lower()


def test_provided_credentials(browser):
    """Test logging in with the user-provided credentials: 'web login' / 'web pass'"""
    username = "web login"
    password = "web pass"
    
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Try registering the user first (just in case they don't exist in the database)
    toggles = browser.find_elements("xpath", "//*[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@name='full_name']").send_keys("Web User")
    browser.find_element("xpath", "//input[@name='username']").send_keys(username)
    browser.find_element("xpath", "//input[@name='email']").send_keys("webuser@example.com")
    browser.find_element("xpath", "//input[@name='password']").send_keys(password)
    browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys(password)
    browser.find_element("xpath", "//input[@name='privacy_consent']").click()
    browser.find_element("xpath", "//button[@type='submit']").click()
    
    time.sleep(2)
    
    # If we are already on dashboard, great!
    # If not (e.g. user already exists), switch to Login page and log in
    if "dashboard" not in browser.current_url:
        toggles = browser.find_elements("xpath", "//*[contains(text(), 'Log in')]")
        if toggles:
            toggles[0].click()
            time.sleep(0.5)
            
        username_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(("xpath", "//input[@placeholder='Enter username']"))
        )
        password_input = browser.find_element("xpath", "//input[@placeholder='Enter password']")
        submit_btn = browser.find_element("xpath", "//button[@type='submit']")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        submit_btn.click()
        
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    browser.execute_script("window.localStorage.clear();")

