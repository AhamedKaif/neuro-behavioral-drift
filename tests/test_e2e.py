import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_full_e2e_flow(browser):
    """Complete End-to-End Workflow: Register -> Predict (Sandbox) -> Logout"""
    
    unique_username = f"e2e_{uuid.uuid4().hex[:6]}"
    
    # 1. Registration
    browser.get("http://localhost:5173/login")
    
    # Switch to registration
    register_toggle = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register now')]"))
    )
    browser.execute_script("arguments[0].click();", register_toggle)
    
    # Fill registration form
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']"))).send_keys("E2E Test User")
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(unique_username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys("password123")
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, "//input[@name='privacy_consent']"))
    
    browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, "//button[@type='submit']"))
    
    # 2. Wait for dashboard redirect (Registration auto-logs in)
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    
    # 3. Model Telemetry / Prediction
    # Force cognitive fatigue in the sandbox to generate a prediction
    fatigue_label = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]"))
    )
    browser.execute_script("arguments[0].click();", fatigue_label)
    
    transmit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    browser.execute_script("arguments[0].click();", transmit_btn)
    
    # Wait for the backend to ingest successfully
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Ingested Successfully')]"))
    )
    
    # 4. Logout
    # Click the Disconnect button on the dashboard
    disconnect_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Disconnect')]"))
    )
    browser.execute_script("arguments[0].click();", disconnect_btn)
    
    # Verify redirected back to login page
    WebDriverWait(browser, 10).until(EC.url_contains("login"))

