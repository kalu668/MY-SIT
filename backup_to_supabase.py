#!/usr/bin/env python
"""
Automated Database Backup Script for Supabase
Runs daily to backup the database and store backups locally
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Django setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elite_wealth_capital.settings')

import django
django.setup()

from django.core.management import call_command

def backup_database():
    """Create a JSON backup of the database"""
    
    # Create backups directory if it doesn't exist
    backup_dir = Path(__file__).parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Backup filename
    backup_file = backup_dir / f'supabase_backup_{timestamp}.json'
    
    print(f"🔄 Starting backup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Backup location: {backup_file}")
    
    try:
        # Use Django's dumpdata command to create backup
        with open(backup_file, 'w') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--indent', '2',
                stdout=f,
                exclude=[
                    'contenttypes',
                    'auth.permission',
                    'sessions.session',
                    'admin.logentry'
                ]
            )
        
        # Get file size
        file_size = backup_file.stat().st_size / 1024  # KB
        
        print(f"✅ Backup completed successfully!")
        print(f"📊 Backup size: {file_size:.2f} KB")
        print(f"📄 File: {backup_file.name}")
        
        # Keep only last 7 backups (delete older ones)
        cleanup_old_backups(backup_dir, keep_count=7)
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")
        return False

def cleanup_old_backups(backup_dir, keep_count=7):
    """Keep only the most recent backups"""
    
    # Get all backup files
    backup_files = sorted(
        backup_dir.glob('supabase_backup_*.json'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    # Delete old backups
    if len(backup_files) > keep_count:
        deleted_count = 0
        for old_backup in backup_files[keep_count:]:
            try:
                old_backup.unlink()
                deleted_count += 1
                print(f"🗑️  Deleted old backup: {old_backup.name}")
            except Exception as e:
                print(f"⚠️  Could not delete {old_backup.name}: {e}")
        
        if deleted_count > 0:
            print(f"✨ Cleaned up {deleted_count} old backup(s)")

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 ELITE WEALTH CAPITAL - AUTOMATED BACKUP")
    print("=" * 60)
    
    success = backup_database()
    
    print("=" * 60)
    
    sys.exit(0 if success else 1)
