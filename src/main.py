import subprocess
import sys
import os
from datetime import datetime, timedelta
from config import final_branch, release_branch_pattern, max_days_old

working_direcotry_git = os.path.join(os.getcwd(), '.git')

def is_release_branch(branch_name):
    return branch_name.startswith(release_branch_pattern)

def get_final_branch():
    return final_branch

def check_branch_merged(branch_name, final_branch):
    try:
        result = subprocess.run(
            ['git', '--git-dir', working_direcotry_git,'branch', '--merged', final_branch],
            capture_output=True,
            text=True,
            check=True
        )
         
        merged_branches = [branch.strip() for branch in result.stdout.splitlines()]
        return branch_name in merged_branches
    except subprocess.CalledProcessError as e:
        print(f"Error checking merged branches: {e}")
        return False

def get_recent_release_branches(max_days_old):
    try:
        result = subprocess.run(
            ['git', '--git-dir', working_direcotry_git, 'for-each-ref', '--sort=-committerdate', '--format=%(refname:short) %(committerdate:iso8601)', 'refs/heads/'],
            capture_output=True,
            text=True,
            check=True
        )
        branches = result.stdout.splitlines()
        recent_branches = []
        cutoff_date = datetime.now() - timedelta(days=max_days_old)
        for branch in branches:
            branch_name, commit_date = branch.split(' ', 1)
            commit_date = datetime.fromisoformat(commit_date).replace(tzinfo=None)
            if is_release_branch(branch_name) and commit_date > cutoff_date:
                recent_branches.append(branch_name)
        return recent_branches
    except subprocess.CalledProcessError as e:
        print(f"Error getting branches: {e}")
        return []

def main():
    recent_branches = get_recent_release_branches(max_days_old)
    final_branch = get_final_branch()
    
    if not recent_branches:
        print("No recent release branches found.")
        sys.exit(0)

    all_merged = True
    for branch in recent_branches:
        if not check_branch_merged(branch, final_branch):
            print(f"{branch} has not been merged into {final_branch}.")
            all_merged = False

    if all_merged:
        print("All recent release branches have been merged.")
    else:
        print("Some recent release branches have not been merged.")

if __name__ == "__main__":
    main()