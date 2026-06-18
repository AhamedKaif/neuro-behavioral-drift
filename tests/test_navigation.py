from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

def test_unauthenticated_navigation(browser):
    """Test that navigating to dashboard without login redirects to login page."""
    browser.get("https://neuro-behavioral-drift.onrender.com/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("https://neuro-behavioral-drift.onrender.com/dashboard")
    WebDriverWait(browser, 10).until(EC.url_contains("login"))

def test_navigation_links(browser, login_helper):
    """Test navigating using navbar links."""
    login_helper()
    
    # Click Model Telemetry
    telemetry_link = browser.find_element("xpath", "//a[contains(., 'Model Telemetry')]")
    telemetry_link.click()
    WebDriverWait(browser, 10).until(EC.url_contains("model-telemetry"))
    
    # Click Dashboard
    dashboard_link = browser.find_element("xpath", "//a[contains(., 'Dashboard')]")
    dashboard_link.click()
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))


