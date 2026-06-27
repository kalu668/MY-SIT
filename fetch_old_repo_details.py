#!/usr/bin/env python3
"""
Fetch old repository details from GitHub
"""
import requests
import json

TOKEN = "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"
OWNER = "KINGSACCOUNT1"
REPO = "coach-jv"
OLD_COMMIT = "d63b45cd751cd366a774d939fb7d6886c931c21c"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

print("🔍 Fetching old repository details from commit:", OLD_COMMIT[:7])
print("=" * 70)

# Get file tree
tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{OLD_COMMIT}?recursive=1"
response = requests.get(tree_url, headers=headers)

if response.status_code == 200:
    tree = response.json()
    files = [item['path'] for item in tree.get('tree', []) if item['type'] == 'blob']
    
    print(f"\n📁 Total files in old repo: {len(files)}\n")
    
    # Look for important files
    important_files = [
        'cryptoplatform/settings.py',
        '.env.example',
        'README.md',
        'templates/base.html',
        'templates/home.html'
    ]
    
    for file_path in important_files:
        if file_path in files:
            print(f"\n{'='*70}")
            print(f"📄 Fetching: {file_path}")
            print('='*70)
            
            file_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}?ref={OLD_COMMIT}"
            file_response = requests.get(file_url, headers=headers)
            
            if file_response.status_code == 200:
                import base64
                content = base64.b64decode(file_response.json()['content']).decode('utf-8')
                
                # Extract relevant lines
                lines = content.split('\n')
                relevant_lines = []
                
                for i, line in enumerate(lines):
                    if any(keyword in line.lower() for keyword in ['coachjv', 'email', 'domain', 'allowed_hosts', 'csrf_trusted']):
                        relevant_lines.append(f"{i+1}: {line}")
                
                if relevant_lines:
                    print("\n🔍 Found relevant configuration:")
                    for line in relevant_lines[:30]:
                        print(line)
                else:
                    print("No coachjv references found")
            else:
                print(f"❌ Failed to fetch file: {file_response.status_code}")

print("\n" + "=" * 70)
