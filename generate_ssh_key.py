#!/usr/bin/env python3
"""
Generate SSH ED25519 key pair for GitHub authentication
"""
import os
import subprocess
import sys

def generate_ssh_key():
    """Generate SSH key using available methods"""
    
    ssh_dir = os.path.expanduser("~/.ssh")
    key_file = os.path.join(ssh_dir, "id_ed25519_github")
    pub_key_file = key_file + ".pub"
    
    # Ensure .ssh directory exists
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir, mode=0o700)
        print(f"Created directory: {ssh_dir}")
    
    # Check if key already exists
    if os.path.exists(key_file):
        print(f"⚠️  SSH key already exists at: {key_file}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return False
    
    # Try different methods to generate key
    methods = [
        # Method 1: Direct ssh-keygen call
        ['ssh-keygen', '-t', 'ed25519', '-C', 'support@coachjv.com', '-f', key_file, '-N', ''],
        # Method 2: Using /usr/bin/ssh-keygen explicitly
        ['/usr/bin/ssh-keygen', '-t', 'ed25519', '-C', 'support@coachjv.com', '-f', key_file, '-N', ''],
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"\nAttempting method {i}: {' '.join(method[:3])}...")
            result = subprocess.run(
                method,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ SSH key generated successfully!")
                print(f"Private key: {key_file}")
                print(f"Public key: {pub_key_file}")
                
                # Display the public key
                if os.path.exists(pub_key_file):
                    with open(pub_key_file, 'r') as f:
                        pub_key_content = f.read().strip()
                    print(f"\n{'='*70}")
                    print("📋 YOUR PUBLIC KEY (Add this to GitHub):")
                    print('='*70)
                    print(pub_key_content)
                    print('='*70)
                    
                    # Save to a file for easy access
                    output_file = os.path.expanduser("~/github_public_key.txt")
                    with open(output_file, 'w') as f:
                        f.write(pub_key_content)
                    print(f"\n✅ Public key also saved to: {output_file}")
                
                return True
            else:
                print(f"❌ Method {i} failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  Method {i} timed out")
        except FileNotFoundError:
            print(f"❌ Method {i}: ssh-keygen not found")
        except PermissionError as e:
            print(f"❌ Method {i}: Permission denied - {e}")
        except Exception as e:
            print(f"❌ Method {i} failed: {e}")
    
    print("\n❌ All methods failed. Key generation not possible on this system.")
    print("\n🔧 ALTERNATIVE SOLUTION:")
    print("=" * 70)
    print("You can use the existing enterprise key for GitHub.com:")
    enterprise_pub = os.path.expanduser("~/.ssh/github_enterprise_key.pub")
    if os.path.exists(enterprise_pub):
        with open(enterprise_pub, 'r') as f:
            print(f.read().strip())
        print("\nOR generate a key on your local machine and copy it here.")
    print("=" * 70)
    
    return False

if __name__ == "__main__":
    print("🔑 GitHub SSH Key Generator")
    print("=" * 70)
    result = generate_ssh_key()
    sys.exit(0 if result else 1)
