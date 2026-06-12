import time
from selenium.webdriver.common.keys import Keys

def test_sandbox_input_updates(browser, login_helper):
    """Type into the interactive sandbox text area and verify metrics update."""
    login_helper()
    
    # Wait for trackers to initialize
    time.sleep(3)
    
    # Find chars counter before typing
    chars_label = browser.find_element("xpath", "//span[contains(text(), 'Chars:')]//span")
    initial_chars = int(chars_label.text)
    
    textarea = browser.find_element("xpath", "//textarea[contains(@placeholder, 'Start typing text here')]")
    textarea.send_keys("Hello world")
    
    time.sleep(1)
    new_chars = int(chars_label.text)
    assert new_chars > initial_chars

def test_force_fatigue_toggle(browser, login_helper):
    """Toggle the Force Cognitive Fatigue Simulation checkbox."""
    login_helper()
    
    checkbox = browser.find_element("xpath", "//input[@type='checkbox']")
    assert not checkbox.is_selected()
    
    # Click the label to toggle checkbox
    label = browser.find_element("xpath", "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]")
    label.click()
    
    assert checkbox.is_selected()

def test_empty_sandbox_submission(browser, login_helper):
    """Try transmitting metrics without typing anything."""
    login_helper()
    
    transmit_btn = browser.find_element("xpath", "//button[contains(., 'Transmit Metrics')]")
    transmit_btn.click()
    time.sleep(1)
    
    # It should succeed even if empty (since live metrics have defaults)
    success_msg = browser.find_element("xpath", "//button[contains(., 'Ingested Successfully')]")
    assert success_msg.is_displayed()

def test_sandbox_reset_trackers(browser, login_helper):
    """Type text into the sandbox and then reset trackers to verify counters clear."""
    login_helper()
    
    # Wait for trackers to initialize
    time.sleep(3)
    
    # Type something to increment the counter
    textarea = browser.find_element("xpath", "//textarea[contains(@placeholder, 'Start typing text here')]")
    textarea.send_keys("Testing reset feature")
    time.sleep(1)
    
    # Verify chars incremented
    chars_label = browser.find_element("xpath", "//span[contains(text(), 'Chars:')]//span")
    assert int(chars_label.text) > 0
    
    # Click the refresh/reset button (it has title="Reset trackers")
    reset_btn = browser.find_element("xpath", "//button[@title='Reset trackers']")
    reset_btn.click()
    time.sleep(1)
    
    # Verify chars are back to 0
    chars_label_after = browser.find_element("xpath", "//span[contains(text(), 'Chars:')]//span")
    assert int(chars_label_after.text) == 0
