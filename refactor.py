import os
import re

for file in os.listdir('tests'):
    if file.startswith('test_') and file.endswith('.py'):
        with open(f'tests/{file}', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'from selenium.webdriver.support.ui import WebDriverWait' not in content:
            content = 'from selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\n' + content
            
        # Replace time.sleep followed by assert url with WebDriverWait
        pattern = r'time\.sleep\([\d\.]+\)\s*assert\s+[\"\']([^\"\']+)[\"\']\s+in\s+browser\.current_url'
        replacement = r'WebDriverWait(browser, 10).until(EC.url_contains("\1"))'
        content = re.sub(pattern, replacement, content)
        
        with open(f'tests/{file}', 'w', encoding='utf-8') as f:
            f.write(content)
