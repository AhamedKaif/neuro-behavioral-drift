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
    
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys(password)
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
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys(password)
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(2)
    
    assert "dashboard" in browser.current_url
    browser.execute_script("window.localStorage.clear();")

def test_invalid_password(browser):
    """Test logging in with an invalid password."""
    username, _ = setup_user(browser)
    
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(username)
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys("wrongpassword")
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(2)
    
    assert "login" in browser.current_url
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_invalid_username(browser):
    """Test logging in with a non-existent username."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@placeholder='Enter username']").send_keys(f"nonexistent_{uuid.uuid4().hex[:6]}")
    browser.find_element("xpath", "//input[@placeholder='Enter password']").send_keys("password")
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(2)
    
    assert "login" in browser.current_url
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "invalid" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_login_empty_fields(browser):
    """Test logging in with empty fields."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Log in')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(1)
    
    error_msg = browser.find_element("xpath", "//div[contains(@class, 'text-red-400')]")
    assert "fill in all fields" in error_msg.text.lower()
