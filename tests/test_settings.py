from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_model_telemetry_loads(browser, login_helper):
    """Verify that the Model Telemetry page loads and displays core elements."""
    login_helper()
    
    # Navigate to Model Telemetry
    telemetry_link = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Model Telemetry')]"))
    )
    telemetry_link.click()
    
    # Verify title
    title = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Model Telemetry & Calibration')]"))
    )
    assert title.is_displayed()
    
    # Verify Accuracy Card
    accuracy = browser.find_element(By.XPATH, "//span[contains(., 'Overall Accuracy')]")
    assert accuracy.is_displayed()
    
    # Verify Feature Importances
    feature_title = browser.find_element(By.XPATH, "//h3[contains(., 'Decision Tree Feature Importances')]")
    assert feature_title.is_displayed()
