#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main orchestration script that runs the complete workflow:
1. List OneDrive files
2. Generate HTML players
3. Deploy to GitHub
4. Display public URLs
"""

import subprocess
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*60)
    print(description.upper())
    print("="*60 + "\n")

    result = subprocess.run([sys.executable, script_name])

    if result.returncode != 0:
        print(f"\n❌ Error running {script_name}")
        return False

    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           KARNLADA SONGS - COMPLETE WORKFLOW             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Step 1: List OneDrive files
    if not run_script("list_onedrive_files.py", "Step 1: Listing OneDrive Files"):
        print("\n⚠️  Please edit list_onedrive_files.py to add your music files")
        print("Then run this script again.")
        return

    # Check if we have files to process
    if not os.path.exists('onedrive_files.json'):
        print("\n❌ Error: onedrive_files.json not created")
        return

    # Step 2: Generate HTML players
    if not run_script("generate_players.py", "Step 2: Generating HTML Music Players"):
        return

    # Step 3: Deploy to GitHub
    print("\n" + "="*60)
    print("STEP 3: DEPLOYING TO GITHUB")
    print("="*60)

    deploy_choice = input("\nDo you want to deploy to GitHub now? (y/n): ").strip().lower()

    if deploy_choice == 'y':
        if not run_script("deploy.py", "Step 3: Deploying to GitHub"):
            print("\n❌ Deployment failed")
            print("\nYou can try deploying manually later by running:")
            print("  python deploy.py")
            return
    else:
        print("\nSkipping deployment. You can deploy later by running:")
        print("  python deploy.py")

    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*60)

    print("\n📋 NEXT STEPS:")
    print("\n1. If you deployed: Wait a few minutes for GitHub Pages to update")
    print("2. Make sure GitHub Pages is enabled in your repository settings:")
    print("   https://github.com/kacharuk/karnlada_songs/settings/pages")
    print("3. Share your music player URLs on Messenger!")
    print("\nTo add more songs:")
    print("  - Edit list_onedrive_files.py")
    print("  - Run: python run_all.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        sys.exit(1)
