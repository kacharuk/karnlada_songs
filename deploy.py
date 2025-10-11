#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to deploy HTML files to GitHub and get their public URLs.
"""

import subprocess
import json
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def run_command(command, description=""):
    """Run a shell command and return the result"""
    if description:
        print(f"\n{description}")

    print(f"Running: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_git_config():
    """Check if git is configured"""
    try:
        result = subprocess.run(
            "git config user.name",
            shell=True,
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            print("\nGit user.name not configured!")
            print("Please run:")
            print('  git config user.name "Your Name"')
            print('  git config user.email "your.email@example.com"')
            return False
        return True
    except:
        return False

def deploy_to_github(commit_message="Update music players"):
    """Deploy the generated HTML files to GitHub"""

    print("="*60)
    print("DEPLOYING TO GITHUB")
    print("="*60)

    # Check git config
    if not check_git_config():
        print("\nPlease configure git first and try again.")
        return False

    # Check if docs directory exists
    if not os.path.exists('docs'):
        print("Error: docs directory not found!")
        print("Please run generate_players.py first.")
        return False

    # Add all files
    if not run_command("git add .", "Adding files to git..."):
        return False

    # Check if there are changes to commit
    result = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        print("\nNo changes to commit. Everything is up to date.")
        return True

    # Commit changes
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes..."):
        return False

    # Check if main branch exists
    result = subprocess.run(
        "git branch --show-current",
        shell=True,
        capture_output=True,
        text=True
    )

    current_branch = result.stdout.strip()

    if not current_branch:
        # First commit, need to create main branch
        print("\nCreating main branch...")
        run_command("git branch -M main")

    # Push to GitHub
    print("\nPushing to GitHub...")
    print("Note: You may need to authenticate with GitHub")

    if not run_command("git push -u origin main", "Pushing to remote..."):
        print("\nPush failed. This might be because:")
        print("1. You need to authenticate with GitHub")
        print("2. The repository doesn't exist yet")
        print("3. You don't have permission to push")
        print("\nTo fix authentication issues:")
        print("- Use GitHub CLI: gh auth login")
        print("- Or use personal access token")
        print("- Or set up SSH keys")
        return False

    print("\n" + "="*60)
    print("DEPLOYMENT SUCCESSFUL!")
    print("="*60)

    # Configure GitHub Pages if needed
    print("\nIMPORTANT: Make sure GitHub Pages is enabled!")
    print("\nTo enable GitHub Pages:")
    print("1. Go to: https://github.com/kacharuk/karnlada_songs/settings/pages")
    print("2. Under 'Source', select 'main' branch")
    print("3. Select '/docs' folder")
    print("4. Click 'Save'")
    print("\nYour site will be available at:")
    print("https://kacharuk.github.io/karnlada_songs/")

    return True

def display_urls():
    """Display all generated URLs"""

    if not os.path.exists('generated_urls.json'):
        print("No URLs file found. Please run the full workflow first.")
        return

    with open('generated_urls.json', 'r', encoding='utf-8') as f:
        files = json.load(f)

    print("\n" + "="*60)
    print("PUBLIC URLS FOR YOUR MUSIC PLAYERS")
    print("="*60)

    for idx, file in enumerate(files, 1):
        print(f"\n{idx}. {file['title']} - {file['artist']}")
        print(f"   URL: {file['url']}")
        print(f"   (Share this link on Messenger)")

    print("\n" + "="*60)
    print(f"\nIndex page: https://kacharuk.github.io/karnlada_songs/")
    print("\nNote: It may take a few minutes for GitHub Pages to update")
    print("      after pushing changes.")
    print("="*60)

def main():
    commit_message = "Update music players"

    if len(sys.argv) > 1:
        commit_message = sys.argv[1]

    success = deploy_to_github(commit_message)

    if success:
        display_urls()
    else:
        print("\nDeployment failed. Please fix the errors and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
