import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@pytest.fixture(scope="session")
def browser():
    """Sets up a Chrome WebDriver instance for the entire test session."""
    options = webdriver.ChromeOptions()
    if os.environ.get('CI') == 'true':
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
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
            os.makedirs("reports/screenshots", exist_ok=True)
            file_name = f"reports/screenshots/screenshot_{item.name}.png"
            if "browser" in item.funcargs:
                driver = item.funcargs["browser"]
                try:
                    driver.save_screenshot(file_name)
                    # Attach to HTML report
                    if hasattr(item.config, '_html') and item.config._html:
                        pytest_html = item.config.pluginmanager.getplugin('html')
                        extra = getattr(report, 'extra', [])
                        extra.append(pytest_html.extras.image(file_name))
                        report.extra = extra
                except Exception as e:
                    print(f"Failed to capture screenshot: {e}")

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
            
        # 1. Try logging in first
        try:
            username_input = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located(("xpath", "//input[@placeholder='Enter username']"))
            )
            password_input = browser.find_element("xpath", "//input[@placeholder='Enter password']")
            submit_btn = browser.find_element("xpath", "//button[@type='submit']")
            
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            submit_btn.click()
            
            # Wait up to 3 seconds for dashboard to confirm successful login
            WebDriverWait(browser, 3).until(EC.url_contains("dashboard"))
        except Exception:
            # Login failed (probably user doesn't exist), so try registering
            if "dashboard" not in browser.current_url:
                register_toggle = browser.find_elements("xpath", "//*[contains(text(), 'Register now')]")
                if register_toggle:
                    register_toggle[0].click()
                    time.sleep(0.5)
                
                browser.find_element("xpath", "//input[@name='full_name']").send_keys("Test User")
                browser.find_element("xpath", "//input[@name='username']").send_keys(username)
                browser.find_element("xpath", "//input[@name='email']").send_keys(f"{username}@example.com")
                browser.find_element("xpath", "//input[@name='password']").send_keys(password)
                browser.find_element("xpath", "//input[@name='confirmPassword']").send_keys(password)
                consent = browser.find_element("xpath", "//input[@name='privacy_consent']")
                if not consent.is_selected():
                    consent.click()
                browser.find_element("xpath", "//button[@type='submit']").click()
                
                # Wait for registration redirect
                WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    return _login
