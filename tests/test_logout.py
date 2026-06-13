import time

def test_logout(browser, login_helper):
    """Test clicking the logout/disconnect button."""
    login_helper()
    
    disconnect_btn = browser.find_element("xpath", "//button[contains(., 'Disconnect')]")
    disconnect_btn.click()
    time.sleep(1)
    
    assert "login" in browser.current_url
    
    # Ensure cannot go back
    browser.get("http://localhost:5173/dashboard")
    time.sleep(1)
    assert "login" in browser.current_url
