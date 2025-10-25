import yaml
import re

try:
    with open('master-plan/master-plan.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
    if match:
        yaml.safe_load(match.group(1))
        print('✅ YAML is valid')
    else:
        print('❌ Could not find YAML front matter.')
except yaml.YAMLError as e:
    print(f'❌ YAML is invalid: {e}')
except Exception as e:
    print(f'An error occurred: {e}')
