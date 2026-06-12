import time

def test_profile_loads(browser, login_helper):
    """Test that the user can navigate to the profile page."""
    login_helper()
    
    # Click Profile icon in navbar
    profile_link = browser.find_element("xpath", "//a[@href='/profile']")
    profile_link.click()
    time.sleep(1)
    
    assert "profile" in browser.current_url
    assert "Profile Management" in browser.page_source

def test_edit_profile(browser, login_helper):
    """Test that a user can edit their profile fields."""
    login_helper()
    
    browser.get("http://localhost:5173/profile")
    time.sleep(1)
    
    # Click Edit Profile
    edit_btn = browser.find_element("xpath", "//button[contains(text(), 'Edit Profile')]")
    browser.execute_script("arguments[0].click();", edit_btn)
    time.sleep(0.5)
    
    # Change stress level
    stress_input = browser.find_element("xpath", "//input[@name='stress_level']")
    # Move slider or send keys (for range it might be tricky, let's just send keys to another field)
    # Let's change institution
    institution_input = browser.find_element("xpath", "//input[@name='institution']")
    institution_input.clear()
    institution_input.send_keys("Automated Test University")
    
    # Save
    save_btn = browser.find_element("xpath", "//button[contains(text(), 'Save Changes')]")
    browser.execute_script("arguments[0].click();", save_btn)
    
    # Wait for save (success message or Edit Profile button reappears)
    time.sleep(2)
    
    # Verify the value persists after refresh
    browser.refresh()
    time.sleep(1)
    
    assert "Automated Test University" in browser.page_source
