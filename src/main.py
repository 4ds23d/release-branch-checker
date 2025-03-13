import subprocess
import sys
import os
from datetime import datetime, timedelta

working_direcotry_git = os.path.join(os.getcwd(), '.git')

def is_release_branch(branch_name, release_branch_pattern):
    return branch_name.startswith(release_branch_pattern)

def run_command(command, print_error=True) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        if print_error:
            print(f"Error running command: {e}")
        return ""

def run_git_command(command, print_error = True) -> str:
    return run_command(['git', '--git-dir', working_direcotry_git] + command, print_error=print_error)

def check_branch_merged(branch_name, final_branch):
    try:
        result = run_git_command(
            ['branch', '--merged', final_branch]
        )
        merged_branches = [branch.strip() for branch in result.splitlines()]
        return branch_name in merged_branches
    except subprocess.CalledProcessError as e:
        print(f"Error checking merged branches: {e}")
        return False

def get_recent_release_branches(max_days_old, release_branch_pattern):
    try:
        result = run_git_command(
            ['for-each-ref', '--sort=-committerdate', '--format=%(refname:short) %(committerdate:iso8601)', 'refs/heads/'],
        )
        branches = result.splitlines()
        recent_branches = []
        cutoff_date = datetime.now() - timedelta(days=max_days_old)
        for branch in branches:
            branch_name, commit_date = branch.split(' ', 1)
            commit_date = datetime.fromisoformat(commit_date).replace(tzinfo=None)
            if is_release_branch(branch_name, release_branch_pattern) and commit_date > cutoff_date:
                recent_branches.append(branch_name)
        return recent_branches
    except subprocess.CalledProcessError as e:
        print(f"Error getting branches: {e}")
        return []

def set_git_config():
    try:
        final_branch = input("Enter the final branch name: ")
        release_branch_pattern = input("Enter the release branch pattern: ")
        max_days_old = input("Enter the maximum number of days old for release branches: ")

        run_git_command(
            ['config', '--local', 'releasechecker.finalBranch', final_branch]
        )
        run_git_command(
            ['config', '--local', 'releasechecker.releaseBranchPattern', release_branch_pattern]
        )
        run_git_command(
            ['config', '--local', 'releasechecker.maxDaysOld', str(max_days_old)]
        )
    except subprocess.CalledProcessError as e:
        print(f"Error setting git config: {e}")
        sys.exit(1)

def get_git_config():
    try:
        final_branch = run_git_command(
            [ 'config', '--local', 'releasechecker.finalBranch']
        ).strip()
        release_branch_pattern = run_git_command(
            ['config', '--local', 'releasechecker.releaseBranchPattern']
        ).strip()
        max_days_old = int(run_git_command(
            ['config', '--local', 'releasechecker.maxDaysOld']
        ).strip())
        return final_branch, release_branch_pattern, max_days_old
    except subprocess.CalledProcessError as e:
        print(f"Error getting git config: {e}")
        sys.exit(1)

def main():
    if not run_git_command(['config', '--local', '--get', 'releasechecker.finalBranch'], print_error=False):
        set_git_config()

    final_branch, release_branch_pattern, max_days_old = get_git_config()

    recent_branches = get_recent_release_branches(max_days_old, release_branch_pattern)
    
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