import os
import re

for root, _, files in os.walk('tests'):
    for file in files:
        if not file.endswith('.py'): continue
        path = os.path.join(root, file)
        with open(path, 'r') as f:
            content = f.read()
        
        content = re.sub(r'(browser\.find_element\([^)]+\))\.click\(\)', r'browser.execute_script("arguments[0].click();", \1)', content)
        content = re.sub(r'^(\s*)([a-zA-Z0-9_]+(?:\[\d+\])?)\.click\(\)', r'\1browser.execute_script("arguments[0].click();", \2)', content, flags=re.MULTILINE)
        
        with open(path, 'w') as f:
            f.write(content)

print("Done fixing clicks!")
