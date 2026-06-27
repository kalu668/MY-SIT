#!/usr/bin/env python3
"""
Generate SSH ED25519 key pair using Python cryptography library
"""
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64
import os

def generate_ssh_ed25519_key():
    """Generate ED25519 SSH key pair"""
    
    print("🔑 Generating SSH ED25519 Key Pair...")
    print("=" * 70)
    
    # Generate private key
    private_key = ed25519.Ed25519PrivateKey.generate()
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize private key to OpenSSH format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key to OpenSSH format
    public_ssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    
    # Add comment to public key
    public_key_with_comment = public_ssh.decode('utf-8') + ' support@coachjv.com'
    
    # Save keys
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    
    private_key_path = os.path.join(ssh_dir, "id_ed25519_github")
    public_key_path = os.path.join(ssh_dir, "id_ed25519_github.pub")
    
    # Write private key
    with open(private_key_path, 'wb') as f:
        f.write(private_pem)
    os.chmod(private_key_path, 0o600)
    
    # Write public key
    with open(public_key_path, 'w') as f:
        f.write(public_key_with_comment)
    os.chmod(public_key_path, 0o644)
    
    print(f"✅ Private key saved to: {private_key_path}")
    print(f"✅ Public key saved to: {public_key_path}")
    print("\n" + "=" * 70)
    print("📋 YOUR PUBLIC KEY (Copy this to GitHub):")
    print("=" * 70)
    print(public_key_with_comment)
    print("=" * 70)
    
    # Also save to an easy-to-access file
    output_file = os.path.expanduser("~/GITHUB_PUBLIC_KEY.txt")
    with open(output_file, 'w') as f:
        f.write(public_key_with_comment + '\n')
    
    print(f"\n✅ Public key also saved to: {output_file}")
    
    # Update SSH config
    config_path = os.path.join(ssh_dir, "config")
    github_config = f"""

# GitHub.com SSH Configuration
Host github.com
    HostName github.com
    User git
    IdentityFile {private_key_path}
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
"""
    
    # Check if config exists and doesn't already have github.com entry
    add_config = True
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            if 'github.com' in f.read():
                add_config = False
                print("\n⚠️  SSH config already has github.com entry")
    
    if add_config:
        with open(config_path, 'a') as f:
            f.write(github_config)
        print(f"\n✅ Updated SSH config: {config_path}")
    
    print("\n" + "=" * 70)
    print("📝 NEXT STEPS:")
    print("=" * 70)
    print("1. Copy the public key above")
    print("2. Go to: https://github.com/settings/ssh/new")
    print("3. Add a title (e.g., 'Coach JV Server')")
    print("4. Paste the public key")
    print("5. Click 'Add SSH key'")
    print("\nThen you can push your code:")
    print("   cd ~/coach")
    print("   git push -f origin master")
    print("=" * 70)

if __name__ == "__main__":
    try:
        generate_ssh_ed25519_key()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
