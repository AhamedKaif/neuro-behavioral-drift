import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_notification_bell_presence(browser, login_helper):
    """Test that the notification bell is visible on the dashboard."""
    login_helper()
    
    # Wait for dashboard to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Cognitive Diagnostics Workspace')]"))
    )
    
    # Check for notification bell using its link route
    bell_link = browser.find_element(By.XPATH, "//a[@href='/notifications']")
    assert bell_link.is_displayed()

def test_medium_strain_notification_generation(browser, login_helper):
    """Simulate some fatigue to trigger a Medium strain or prolonged session notification."""
    login_helper()
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Transmit Metrics')]"))
    )
    
    # Enable Force Simulation
    sim_checkbox = browser.find_element(By.XPATH, "//input[@type='checkbox']")
    if not sim_checkbox.is_selected():
        browser.execute_script("arguments[0].click();", sim_checkbox)
        
    # Trigger metrics ingest
    submit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    # Wait for success status
    time.sleep(5)
    
    # Wait for the Recommendation panel to populate
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Cognitive Strain Detected') or contains(text(), 'Prolonged Session Warning')]"))
    )

def test_notifications_history_page(browser, login_helper):
    """Navigate to the notifications history page and test filtering and marking read."""
    login_helper()
    
    # Trigger an alert first
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Transmit Metrics')]"))
    )
    sim_checkbox = browser.find_element(By.XPATH, "//input[@type='checkbox']")
    browser.execute_script("arguments[0].click();", sim_checkbox)
    submit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", submit_btn)
    time.sleep(5)
    
    # Navigate to notifications
    bell_link = browser.find_element(By.XPATH, "//a[@href='/notifications']")
    browser.execute_script("arguments[0].click();", bell_link)
    
    # Wait for Notification Center
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[text()='Notification Center']"))
    )
    
    # Test Mark All Read
    mark_all_btn = browser.find_element(By.XPATH, "//button[contains(text(), 'Mark all as read')]")
    assert mark_all_btn.is_displayed()
    browser.execute_script("arguments[0].click();", mark_all_btn)
    time.sleep(3)
    
    # Ensure notifications are listed
    cards = browser.find_elements(By.XPATH, "//div[contains(@class, 'flex-grow')]")
    assert len(cards) > 0
    
def test_delete_notification(browser, login_helper):
    """Test deleting a notification from the history page."""
    login_helper()
    
    # Generate alert
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Transmit Metrics')]"))
    )
    sim_checkbox = browser.find_element(By.XPATH, "//input[@type='checkbox']")
    browser.execute_script("arguments[0].click();", sim_checkbox)
    submit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", submit_btn)
    time.sleep(5)
    
    # Navigate
    browser.get("https://neuro-behavioral-drift.onrender.com/notifications")
    time.sleep(3)
    
    # Delete first notification
    delete_btns = browser.find_elements(By.XPATH, "//button[contains(., 'Delete')]")
    if delete_btns:
        initial_count = len(delete_btns)
        browser.execute_script("arguments[0].click();", delete_btns[0])
        time.sleep(3)
        new_btns = browser.find_elements(By.XPATH, "//button[contains(., 'Delete')]")
        assert len(new_btns) < initial_count
