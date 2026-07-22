from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

def test_unauthenticated_navigation(browser):
    """Test that navigating to dashboard without login redirects to login page."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/dashboard")
    WebDriverWait(browser, 10).until(EC.url_contains("login"))

def test_navigation_links(browser, login_helper):
    """Test navigating using navbar links."""
    login_helper()
    
    # Click Model Telemetry
    telemetry_link = browser.find_element("xpath", "//a[contains(., 'Model Telemetry')]")
    browser.execute_script("arguments[0].click();", telemetry_link)
    WebDriverWait(browser, 10).until(EC.url_contains("model-telemetry"))
    
    # Click Dashboard
    dashboard_link = browser.find_element("xpath", "//a[contains(., 'Dashboard')]")
    browser.execute_script("arguments[0].click();", dashboard_link)
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))


