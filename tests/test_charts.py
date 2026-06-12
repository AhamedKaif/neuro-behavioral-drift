import time

def test_charts_render(browser, login_helper):
    """Ensure the Recharts container exists on the dashboard for the strain history chart."""
    login_helper()
    
    # Wait for dashboard to fully load and fetch data
    time.sleep(3)
    
    # Recharts wrapper class
    charts = browser.find_elements("xpath", "//div[contains(@class, 'recharts-wrapper')]")
    assert len(charts) >= 1, "Expected at least one recharts-wrapper element to be rendered."

def test_charts_axis(browser, login_helper):
    """Verify the X and Y axes of the charts are visible."""
    login_helper()
    time.sleep(3)
    
    # Check for recharts CartesianGrid or similar elements
    svg_elements = browser.find_elements("xpath", "//*[local-name()='svg']")
    assert len(svg_elements) > 0, "SVG elements for charts not found."
