from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_responsive_layout(browser, login_helper):
    """Verify that the dashboard adapts to mobile dimensions."""
    login_helper()
    
    # Store original window size
    original_size = browser.get_window_size()
    
    try:
        # Resize to mobile portrait (iPhone 12/13 size)
        browser.set_window_size(390, 844)
        
        # Verify dashboard title still visible and wrapped
        title = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Cognitive Diagnostics Workspace')]"))
        )
        assert title.is_displayed()
        
        # Check that the main container fits the screen width (no horizontal scrolling overflow)
        # We can check if stat cards are still visible (they should stack on mobile)
        stat_cards = browser.find_elements(By.XPATH, "//span[contains(@class, 'uppercase tracking-wider')]")
        assert len(stat_cards) >= 4
        assert stat_cards[0].is_displayed()
        
    finally:
        # Restore original window size
        browser.set_window_size(original_size['width'], original_size['height'])
