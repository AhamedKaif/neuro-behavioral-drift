import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Increase all sleeps globally to handle Render spin-ups and React loading better
    content = re.sub(r'time\.sleep\(0\.5\)', 'time.sleep(2)', content)
    content = re.sub(r'time\.sleep\(1\)', 'time.sleep(3)', content)
    content = re.sub(r'time\.sleep\(2\)', 'time.sleep(5)', content)
    
    # Whenever we do browser.get(url), let's ensure we wait for body
    # Actually wait for the submit button to be present if it's the login page
    content = content.replace(
        'browser.get("https://neuro-behavioral-drift.onrender.com/login")\n    time.sleep(3)',
        'browser.get("https://neuro-behavioral-drift.onrender.com/login")\n    WebDriverWait(browser, 20).until(EC.presence_of_element_located(("xpath", "//button[@type=\'submit\']")))\n    time.sleep(2)'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
print('Done fixing sleeps in tests')
