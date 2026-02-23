import subprocess
import os

def push_to_github():
    # Path to your local repository
    repo_dir = r"C:\OneDrive\Public Reports A"
    os.chdir(repo_dir)
    
    try:
        # 1. Stage everything
        subprocess.run(["git", "add", "."], check=True)
        # 2. Commit with a timestamp
        subprocess.run(["git", "commit", "-m", "Automated Sentinel Update"], check=True)
        # 3. Push to main
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return True
    except Exception as e:
        print(f"Sync Failed: {e}")
        return False
