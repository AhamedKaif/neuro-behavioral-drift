import time
import pytest

def test_unauthenticated_navigation(browser):
    """Test that navigating to dashboard without login redirects to login page."""
    browser.get("http://localhost:5173/")
    browser.execute_script("window.localStorage.clear();")
    browser.get("http://localhost:5173/dashboard")
    time.sleep(1)
    
    assert "login" in browser.current_url

def test_navigation_links(browser, login_helper):
    """Test navigating using navbar links."""
    login_helper()
    
    # Click Model Telemetry
    telemetry_link = browser.find_element("xpath", "//a[contains(., 'Model Telemetry')]")
    telemetry_link.click()
    time.sleep(1)
    assert "model-telemetry" in browser.current_url
    
    # Click Dashboard
    dashboard_link = browser.find_element("xpath", "//a[contains(., 'Dashboard')]")
    dashboard_link.click()
    time.sleep(1)
    assert "dashboard" in browser.current_url


