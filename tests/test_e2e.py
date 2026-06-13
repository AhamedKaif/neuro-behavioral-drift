import time
import pytest
from selenium.webdriver.common.by import By

def test_full_e2e_flow(browser):
    """Complete End-to-End Workflow: Register -> Login -> Predict -> Logout"""
    
    # 1. Registration
    browser.get("http://localhost:5173/register")
    browser.find_element(By.ID, "fullName").send_keys("E2E Test User")
    browser.find_element(By.ID, "email").send_keys("e2e_user@example.com")
    browser.find_element(By.ID, "password").send_keys("Password123")
    browser.find_element(By.ID, "confirmPassword").send_keys("Password123")
    browser.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]").click()
    time.sleep(2)
    
    # 2. Login
    browser.get("http://localhost:5173/login")
    browser.find_element(By.ID, "email").send_keys("e2e_user@example.com")
    browser.find_element(By.ID, "password").send_keys("Password123")
    browser.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()
    time.sleep(2)
    assert "dashboard" in browser.current_url
    
    # 3. Model Telemetry / Prediction
    telemetry_link = browser.find_element("xpath", "//a[contains(., 'Model Telemetry')]")
    telemetry_link.click()
    time.sleep(1)
    
    browser.find_element("id", "reactionTime").send_keys("300")
    browser.find_element("id", "errorRate").send_keys("2")
    browser.find_element("id", "focusScore").send_keys("85")
    
    browser.find_element("xpath", "//button[contains(., 'Transmit Metrics')]").click()
    time.sleep(2)
    
    # Check if prediction rendered
    assert len(browser.find_elements("xpath", "//*[contains(text(), 'Cognitive Strain Prediction')]")) > 0
    
    # 4. Logout
    dashboard_link = browser.find_element("xpath", "//a[contains(., 'Dashboard')]")
    dashboard_link.click()
    time.sleep(1)
    
    disconnect_btn = browser.find_element("xpath", "//button[contains(., 'Disconnect')]")
    disconnect_btn.click()
    time.sleep(1)
    assert "login" in browser.current_url
