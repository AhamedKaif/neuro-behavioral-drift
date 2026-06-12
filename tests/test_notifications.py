import time

def test_alert_system_loads(browser, login_helper):
    """Verify the 'Recommendations' panel is visible."""
    login_helper()
    
    alert_header = browser.find_element("xpath", "//h2[contains(text(), 'Recommendations')]")
    assert alert_header.is_displayed()

def test_fatigue_alert_generation(browser, login_helper):
    """Use the fatigue simulation toggle, transmit data, and assert a new alert appears."""
    login_helper()
    
    # Check initial alerts (or clear them)
    try:
        clear_btn = browser.find_element("xpath", "//button[contains(text(), 'Clear All')]")
        clear_btn.click()
        time.sleep(1)
    except:
        pass
        
    # Toggle fatigue
    label = browser.find_element("xpath", "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]")
    label.click()
    
    # Transmit
    transmit_btn = browser.find_element("xpath", "//button[contains(., 'Transmit Metrics')]")
    transmit_btn.click()
    
    time.sleep(3)
    
    # Verify HIGH STRAIN alert is in the feed
    high_strain_alerts = browser.find_elements("xpath", "//span[contains(text(), 'HIGH STRAIN')]")
    assert len(high_strain_alerts) > 0, "Expected a HIGH_STRAIN alert to be generated."
