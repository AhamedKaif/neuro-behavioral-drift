import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import uuid

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
        if username is None:
            username = f"testuser_{uuid.uuid4().hex[:6]}"
            
        browser.get("https://neuro-behavioral-drift.onrender.com/")
        
        try:
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit'] | //a[@href='/profile']"))
            )
        except:
            pass
            
        # Check if already logged in (Dashboard is present)
        if "dashboard" in browser.current_url or len(browser.find_elements(By.XPATH, "//a[@href='/profile']")) > 0:
            return
            
        # Wait for submit button to definitely be there
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            
        # Try registering first
        register_toggle = browser.find_elements(By.XPATH, "//button[contains(text(), 'Register now')]")
        if register_toggle:
            register_toggle[0].click()
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']")))

        browser.find_element(By.XPATH, "//input[@name='full_name']").send_keys("Test User")
        browser.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
        browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{username}@example.com")
        browser.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys(password)
        browser.find_element(By.XPATH, "//input[@name='privacy_consent']").click()
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        
        try:
            # Wait up to 10 seconds for the registration to redirect to dashboard
            WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
        except:
            pass
            
        # If it hasn't redirected, switch to login
        if "dashboard" not in browser.current_url:
            login_toggle = browser.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
            if login_toggle:
                login_toggle[0].click()
            
            username_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']")))
            password_input = browser.find_element(By.XPATH, "//input[@placeholder='Enter password']")
            submit_btn = browser.find_element(By.XPATH, "//button[@type='submit']")
            
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            submit_btn.click()
            
        WebDriverWait(browser, 20).until(EC.url_contains("dashboard"))
    return _login
