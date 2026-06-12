import time

def test_dashboard_loads(browser, login_helper):
    """Verify that the dashboard main elements render correctly."""
    login_helper()
    
    # Check header
    header = browser.find_element("xpath", "//h1[contains(., 'Cognitive Diagnostics Workspace')]")
    assert header.is_displayed()
    
    # Check Sandbox title
    sandbox_title = browser.find_element("xpath", "//h2[contains(., 'Interactive Behavioral Sandbox')]")
    assert sandbox_title.is_displayed()

def test_user_profile_display(browser, login_helper):
    """Verify that the logged-in user's name is displayed correctly."""
    login_helper("testuser", "password123")
    
    user_label = browser.find_element("xpath", "//p[contains(text(), 'Subject ID:')]//span")
    assert "testuser" in user_label.text

def test_dashboard_stats_exist(browser, login_helper):
    """Check for the presence of the 4 main statistic cards."""
    login_helper()
    
    stat_cards = browser.find_elements("xpath", "//span[contains(@class, 'uppercase tracking-wider')]")
    labels = [card.text.upper() for card in stat_cards]
    
    assert any("COGNITIVE STRAIN" in label for label in labels)
    assert any("BEHAVIORAL DRIFT SCORE" in label for label in labels)
    assert any("DAILY SCREEN TIME" in label for label in labels)
    assert any("ACTIVE SESSION" in label for label in labels)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_retrain_model_button(browser, login_helper):
    """Test clicking the Retrain Model button and accepting the alert."""
    login_helper()
    
    retrain_btn = browser.find_element("xpath", "//button[contains(., 'Retrain Model')]")
    retrain_btn.click()
    
    # Wait for alert to appear
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    
    # Switch to alert and accept it
    alert = browser.switch_to.alert
    assert "successfully retrained" in alert.text.lower()
    alert.accept()
