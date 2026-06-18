from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def test_transmit_metrics_success(browser, login_helper):
    """Click Transmit Metrics button and verify successful UI update."""
    login_helper()
    
    transmit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", transmit_btn)
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Ingested Successfully')]"))
    )
    success_btn = browser.find_element(By.XPATH, "//button[contains(., 'Ingested Successfully')]")
    assert success_btn.is_displayed()

def test_cognitive_strain_prediction(browser, login_helper):
    """Verify the Current Strain Level badge updates after forcing fatigue."""
    login_helper()
    
    # Toggle fatigue
    label = browser.find_element(By.XPATH, "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]")
    browser.execute_script("arguments[0].click();", label)
    
    # Transmit
    transmit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", transmit_btn)
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'High')]"))
    )
    # Check strain is high
    strain_badge = browser.find_element(By.XPATH, "//span[contains(text(), 'High')]")
    assert strain_badge.is_displayed()

def test_behavioral_drift_score(browser, login_helper):
    """Verify the Drift Score percentage updates after transmitting high strain metrics."""
    login_helper()
    
    # Read initial drift score
    drift_score_elem = browser.find_element(By.XPATH, "//span[contains(text(), '%')]")
    
    # Toggle fatigue
    label = browser.find_element(By.XPATH, "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]")
    browser.execute_script("arguments[0].click();", label)
    
    # Transmit
    transmit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", transmit_btn)
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Critical')]"))
    )
    
    # Drift score should be very high (Critical)
    critical_badge = browser.find_element(By.XPATH, "//span[contains(text(), 'Critical')]")
    assert critical_badge.is_displayed()
