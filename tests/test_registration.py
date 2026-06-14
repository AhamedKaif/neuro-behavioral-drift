from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

def test_valid_registration(browser):
    """Test registering a new user."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Ensure we are on registration mode
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@name='full_name']").send_keys("Test User")
    
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    browser.find_element("xpath", "//input[@name='username']").send_keys(unique_username)
    browser.find_element("xpath", "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element("xpath", "//input[@name='password']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='privacy_consent']").click()
    
    submit_btn = browser.find_element("xpath", "//button[@type='submit']")
    submit_btn.click()
    
    # Assert successful registration redirects to dashboard
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    
    # Logout for next test
    browser.execute_script("window.localStorage.clear();")

def test_registration_existing_user(browser):
    """Test registering with an already existing username."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Create user first
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@name='full_name']").send_keys("Test User")
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    browser.find_element("xpath", "//input[@name='username']").send_keys(unique_username)
    browser.find_element("xpath", "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element("xpath", "//input[@name='password']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='privacy_consent']").click()
    
    submit_btn = browser.find_element("xpath", "//button[@type='submit']")
    submit_btn.click()
    
    # Logout
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Try registering again
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    browser.find_element("xpath", "//input[@name='full_name']").send_keys("Test User")
    browser.find_element("xpath", "//input[@name='username']").send_keys(unique_username)
    browser.find_element("xpath", "//input[@name='email']").send_keys(f"{unique_username}2@example.com") # different email
    browser.find_element("xpath", "//input[@name='password']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element("xpath", "//input[@name='privacy_consent']").click()
    
    submit_btn = browser.find_element("xpath", "//button[@type='submit']")
    submit_btn.click()
    
    # Should stay on login page and show error
    WebDriverWait(browser, 10).until(EC.url_contains("login"))
    error_msg = WebDriverWait(browser, 5).until(EC.presence_of_element_located(("xpath", "//div[contains(@class, 'text-red-400')]")))
    assert "already exists" in error_msg.text.lower() or "error" in error_msg.text.lower()

def test_registration_empty_fields(browser):
    """Test submitting registration form with empty fields."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    toggles = browser.find_elements("xpath", "//button[contains(text(), 'Register now')]")
    if toggles:
        toggles[0].click()
        time.sleep(0.5)
        
    submit_btn = browser.find_element("xpath", "//button[@type='submit']")
    submit_btn.click()
    
    # Should show error about filling fields
    error_msg = WebDriverWait(browser, 5).until(EC.presence_of_element_located(("xpath", "//div[contains(@class, 'text-red-400')]")))
    assert "fill in all" in error_msg.text.lower()
