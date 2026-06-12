import time

def test_session_expiry_handling(browser, login_helper):
    """Simulate clearing localStorage tokens and reloading to verify redirection to login."""
    login_helper()
    
    # Verify on dashboard
    assert "dashboard" in browser.current_url
    
    # Clear local storage (simulating session expiry)
    browser.execute_script("window.localStorage.removeItem('token');")
    browser.execute_script("window.localStorage.removeItem('user');")
    
    # Reload page
    browser.refresh()
    time.sleep(1)
    
    # Should redirect to login
    assert "login" in browser.current_url

def test_invalid_token_api_rejection(browser):
    """Inject a fake token and verify the app rejects it and logs out."""
    browser.get("http://localhost:5173/login")
    time.sleep(1)
    
    # Inject fake token
    browser.execute_script("window.localStorage.setItem('token', 'fake_invalid_token_12345');")
    browser.execute_script("window.localStorage.setItem('user', JSON.stringify({username: 'fakeuser'}));")
    
    browser.get("http://localhost:5173/dashboard")
    time.sleep(2)
    
    # App should realize token is invalid via API /auth/me and clear it, redirecting to login
    assert "login" in browser.current_url
