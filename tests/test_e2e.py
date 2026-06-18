import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_full_e2e_flow(browser):
    """Complete End-to-End Workflow: Register -> Predict (Sandbox) -> Logout"""
    
    unique_username = f"e2e_{uuid.uuid4().hex[:6]}"
    
    # 1. Registration
    browser.get("https://neuro-behavioral-drift.onrender.com/login")
    
    # Switch to registration
    register_toggle = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register now')]"))
    )
    register_toggle.click()
    
    # Fill registration form
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='full_name']"))).send_keys("E2E Test User")
    browser.find_element(By.XPATH, "//input[@name='username']").send_keys(unique_username)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(f"{unique_username}@example.com")
    browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys("password123")
    browser.find_element(By.XPATH, "//input[@name='privacy_consent']").click()
    
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # 2. Wait for dashboard redirect (Registration auto-logs in)
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    
    # 3. Model Telemetry / Prediction
    # Force cognitive fatigue in the sandbox to generate a prediction
    fatigue_label = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Force Cognitive Fatigue Simulation')]"))
    )
    fatigue_label.click()
    
    transmit_btn = browser.find_element(By.XPATH, "//button[contains(., 'Transmit Metrics')]")
    transmit_btn.click()
    
    # Wait for the backend to ingest successfully
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Ingested Successfully')]"))
    )
    
    # 4. Logout
    # Click the Disconnect button on the dashboard
    disconnect_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Disconnect')]"))
    )
    disconnect_btn.click()
    
    # Verify redirected back to login page
    WebDriverWait(browser, 10).until(EC.url_contains("login"))

