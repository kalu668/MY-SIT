#!/usr/bin/env python3
"""
Deploy coach folder to GitHub using GitHub API
"""
import os
import base64
import json
import subprocess
import requests
from pathlib import Path

# Configuration
GITHUB_TOKEN = "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"
OWNER = "KINGSACCOUNT1"
REPO = "coach-jv"
BRANCH = "master"
COACH_DIR = "/home/ubuntu/coach"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_default_branch():
    """Get the repository's default branch"""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    return "main"

def get_branch_sha(branch):
    """Get the SHA of the latest commit on a branch"""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{branch}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["object"]["sha"]
    return None

def create_tree_from_directory(base_path):
    """Create a tree structure from local directory"""
    tree = []
    base_path = Path(base_path)
    
    # Patterns to ignore
    ignore_patterns = ['.git', '__pycache__', '*.pyc', '.env', 'venv', 'node_modules']
    
    def should_ignore(path):
        path_str = str(path)
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True
        return False
    
    print(f"📂 Scanning directory: {base_path}")
    
    for root, dirs, files in os.walk(base_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_ignore(file_path):
                continue
            
            relative_path = file_path.relative_to(base_path)
            
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Send as plain UTF-8 text (GitHub will handle encoding)
                tree.append({
                    "path": str(relative_path),
                    "mode": "100644",  # Regular file
                    "type": "blob",
                    "content": content
                })
                
                print(f"  ✓ {relative_path}")
                
            except Exception as e:
                print(f"  ✗ {relative_path}: {e}")
    
    return tree

def deploy_to_github():
    """Deploy the coach directory to GitHub"""
    print("=" * 70)
    print("🚀 DEPLOYING COACH FOLDER TO GITHUB")
    print("=" * 70)
    print(f"Repository: {OWNER}/{REPO}")
    print(f"Source: {COACH_DIR}")
    print()
    
    # Step 1: Get default branch
    print("Step 1: Getting repository information...")
    default_branch = get_default_branch()
    print(f"  Default branch: {default_branch}")
    
    # Step 2: Get latest commit SHA
    print("\nStep 2: Getting latest commit...")
    base_sha = get_branch_sha(default_branch)
    if not base_sha:
        print("  ✗ Could not get branch SHA. Creating new branch...")
        # Create initial commit
        base_sha = None
    else:
        print(f"  ✓ Latest commit SHA: {base_sha[:7]}")
    
    # Step 3: Create tree from local directory
    print("\nStep 3: Creating file tree...")
    tree = create_tree_from_directory(COACH_DIR)
    print(f"  ✓ Total files: {len(tree)}")
    
    if len(tree) == 0:
        print("  ✗ No files to upload!")
        return False
    
    # Step 4: Create tree on GitHub
    print("\nStep 4: Uploading tree to GitHub...")
    tree_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees"
    tree_data = {"tree": tree}
    
    response = requests.post(tree_url, headers=headers, json=tree_data)
    if response.status_code not in [200, 201]:
        print(f"  ✗ Failed to create tree: {response.status_code}")
        print(f"  Error: {response.text}")
        return False
    
    tree_sha = response.json()["sha"]
    print(f"  ✓ Tree created: {tree_sha[:7]}")
    
    # Step 5: Create commit
    print("\nStep 5: Creating commit...")
    commit_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits"
    commit_data = {
        "message": "Deploy CoachJVTech Platform\n\n- Domain: coachjvtech.us\n- Email: support@coachjvtech.us, admin@coachjvtech.us, billing@coachjvtech.us\n- Branding: CoachJVTech\n- CSRF trusted origins configured\n- All templates and settings updated\n- Ready for production deployment",
        "tree": tree_sha,
        "parents": [base_sha] if base_sha else []
    }
    
    response = requests.post(commit_url, headers=headers, json=commit_data)
    if response.status_code not in [200, 201]:
        print(f"  ✗ Failed to create commit: {response.status_code}")
        print(f"  Error: {response.text}")
        return False
    
    commit_sha = response.json()["sha"]
    print(f"  ✓ Commit created: {commit_sha[:7]}")
    
    # Step 6: Update branch reference
    print("\nStep 6: Updating branch reference...")
    ref_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{default_branch}"
    ref_data = {
        "sha": commit_sha,
        "force": True  # Force update to replace existing content
    }
    
    response = requests.patch(ref_url, headers=headers, json=ref_data)
    if response.status_code not in [200, 201]:
        print(f"  ✗ Failed to update reference: {response.status_code}")
        print(f"  Error: {response.text}")
        return False
    
    print(f"  ✓ Branch updated successfully!")
    
    # Success!
    print("\n" + "=" * 70)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("=" * 70)
    print(f"🔗 View your repo: https://github.com/{OWNER}/{REPO}")
    print(f"📝 Commit: {commit_sha[:7]}")
    print(f"📊 Files deployed: {len(tree)}")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = deploy_to_github()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
