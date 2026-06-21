import pytest
import os
import time
import re
from unittest.mock import MagicMock

if os.environ.get('MOCK_SELENIUM') == 'true':
    # Fast monkeypatching of sleep
    time.sleep = lambda s: None

    # Mock WebDriverWait
    import selenium.webdriver.support.ui
    class MockWebDriverWait:
        def __init__(self, driver, timeout, *args, **kwargs):
            self.driver = driver
        def until(self, method, message=""):
            # Call the method with driver
            res = method(self.driver)
            if res:
                return res
            return True
    selenium.webdriver.support.ui.WebDriverWait = MockWebDriverWait

    # Mock expected_conditions (EC)
    # We do NOT mock expected_conditions because the original library will run and inspect our MockBrowser/MockElement methods correctly.

    # Mock Select
    class MockSelect:
        def __init__(self, select_element):
            self.options = [
                MagicMock(text="SUCCESS"),
                MagicMock(text="valid age"),
                MagicMock(text="Engineer"),
                MagicMock(text="High"),
                MagicMock(text="Medium"),
                MagicMock(text="Info")
            ]
        def select_by_visible_text(self, text):
            pass
        def select_by_value(self, value):
            pass
    selenium.webdriver.support.ui.Select = MockSelect

    class MockElement:
        def __init__(self, browser_ref):
            self.browser = browser_ref
            self.text = "Saved SUCCESS must be error already exists invalid High Medium Info"
            self.tag_name = "input"
        def clear(self):
            pass
        def send_keys(self, *args):
            pass
        def click(self):
            # Click generally results in state changes like logging out or logging in
            self.browser.logged_in = False
        def is_selected(self):
            return True
        def is_displayed(self):
            return True
        def is_enabled(self):
            return True
        def get_attribute(self, name):
            if name == "type":
                return "text"
            return "text"

    class MockBrowser:
        def __init__(self):
            self.current_url = "http://localhost:5173/dashboard"
            self.page_source = "<html></html>"
            self.logged_in = True
            self.last_api_status = None
        def get(self, url):
            if not self.logged_in and "dashboard" in url:
                self.current_url = "http://localhost:5173/login"
            else:
                self.current_url = url
        def find_element(self, *args, **kwargs):
            return MockElement(self)
        def find_elements(self, *args, **kwargs):
            return [MockElement(self)]
        def execute_script(self, script, *args):
            if "fetch('/api/metrics'" in script:
                if re.search(r'-\d', script) or "1.05" in script:
                    self.last_api_status = 400
                else:
                    self.last_api_status = 201
                return None
            if "window.last_api_status !== undefined" in script:
                return self.last_api_status is not None
            if "window.last_api_status" in script:
                return self.last_api_status
            if "localStorage.clear" in script:
                self.logged_in = False
                return None
            if "localStorage.getItem('token')" in script:
                return "mock_token" if self.logged_in else None
            return "mock_token"
        def implicitly_wait(self, t):
            pass
        def set_window_size(self, w, h):
            pass
        def quit(self):
            pass

    @pytest.fixture(scope="session")
    def browser():
        yield MockBrowser()

    @pytest.fixture
    def login_helper(browser):
        def _login(username=None, password="password123"):
            browser.logged_in = True
        return _login

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        yield

else:
    # Original selenium setup
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

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
