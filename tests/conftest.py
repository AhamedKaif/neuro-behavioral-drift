import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os

@pytest.fixture(scope="session")
def browser():
    """Sets up a Chrome WebDriver instance for the entire test session."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment to run in headless mode
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures a screenshot on test failure and attaches it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = f"screenshot_{item.name}.png"
            if "browser" in item.funcargs:
                driver = item.funcargs["browser"]
                driver.save_screenshot(file_name)
                # Attach to HTML report
                if hasattr(item.config, '_html') and item.config._html:
                    pytest_html = item.config.pluginmanager.getplugin('html')
                    extra = getattr(report, 'extra', [])
                    extra.append(pytest_html.extras.image(file_name))
                    report.extra = extra

@pytest.fixture
def login_helper(browser):
    """Helper fixture to log in a user programmatically via UI."""
    def _login(username=None, password="password123"):
        import uuid
        if username is None:
            username = f"testuser_{uuid.uuid4().hex[:6]}"
            
        browser.get("http://localhost:5173/login")
        time.sleep(1)
        
        # Check if already logged in (Dashboard is present)
        if "dashboard" in browser.current_url:
            return
            
        # Try registering first
        register_toggle = browser.find_element("xpath", "//button[contains(text(), 'Register now')]")
        if register_toggle:
            register_toggle.click()
            time.sleep(0.5)

        username_input = browser.find_element("xpath", "//input[@placeholder='Enter username']")
        password_input = browser.find_element("xpath", "//input[@placeholder='Enter password']")
        submit_btn = browser.find_element("xpath", "//button[@type='submit']")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        submit_btn.click()
        
        time.sleep(2) # Wait for redirect
        
        # If it fails (e.g. exists), switch to login
        if "login" in browser.current_url:
            login_toggle = browser.find_element("xpath", "//button[contains(text(), 'Log in')]")
            if login_toggle:
                login_toggle.click()
                time.sleep(0.5)
            
            username_input = browser.find_element("xpath", "//input[@placeholder='Enter username']")
            password_input = browser.find_element("xpath", "//input[@placeholder='Enter password']")
            submit_btn = browser.find_element("xpath", "//button[@type='submit']")
            
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            submit_btn.click()
            time.sleep(2)
            
        assert "dashboard" in browser.current_url
    return _login
