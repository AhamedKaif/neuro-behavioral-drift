from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def test_protected_route_redirect(browser):
    """Verify that accessing a protected route without auth redirects to login."""
    # Clear localStorage to ensure a logged-out state
    browser.get("http://127.0.0.1:5173/")
    browser.execute_script("window.localStorage.clear();")
    
    # Now attempt to access protected route
    browser.get("http://127.0.0.1:5173/dashboard")
    
    # Wait for redirect to login
    WebDriverWait(browser, 5).until(EC.url_contains("login"))
    
    assert "login" in browser.current_url

def test_unknown_route_redirect(browser, login_helper):
    """Verify that an unknown route handles fallback."""
    login_helper()
    
    # Go to an invalid route
    browser.get("http://127.0.0.1:5173/this-route-does-not-exist")
    
    # It should fallback to dashboard because user is logged in
    WebDriverWait(browser, 15).until(
        lambda driver: "dashboard" in driver.current_url or "login" in driver.current_url
    )
    assert "dashboard" in browser.current_url, f"Expected dashboard, got {browser.current_url}"
