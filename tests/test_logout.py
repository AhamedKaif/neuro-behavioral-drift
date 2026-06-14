from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_logout(browser, login_helper):
    """Test clicking the logout/disconnect button."""
    login_helper()
    
    disconnect_btn = browser.find_element("xpath", "//button[contains(., 'Disconnect')]")
    disconnect_btn.click()
    WebDriverWait(browser, 10).until(EC.url_contains("login"))
    
    # Ensure cannot go back
    browser.get("http://localhost:5173/dashboard")
    WebDriverWait(browser, 10).until(EC.url_contains("login"))
