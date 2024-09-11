import argparse
import logging
import os
import re
import shutil
import subprocess
from datetime import datetime

repo_url = "git@github.com:ministryofjustice/cloud-platform-environments.git"
repo_dir = "./cloud-platform-environments"
namespace_dir = "namespaces/live.cloud-platform.service.justice.gov.uk"
source_namespace_name = "operations-engineering-flask-template"
branch_name_prefix = "add-new-namespace"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def clone_repo():
    """Clone the cloud-platform-environments repository if not already cloned."""
    if not os.path.exists(repo_dir):
        logger.info(f"Cloning repository {repo_url} into {repo_dir}")
        subprocess.run(["git", "clone", repo_url], check=True)
    else:
        logger.info(f"Repository already cloned at {repo_dir}")


def create_new_branch(new_namespace_name):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"{branch_name_prefix}/{new_namespace_name}-{timestamp}"
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_dir, check=True)
    logger.info(f"Created and switched to new branch: {branch_name}")
    return branch_name


def copy_namespace_dir(new_namespace_name):
    """Copy the existing namespace template directory to a new directory."""
    source_namespace_path = os.path.join(repo_dir, namespace_dir, source_namespace_name)
    new_namespace_path = os.path.join(repo_dir, namespace_dir, new_namespace_name)

    if not os.path.exists(source_namespace_path):
        logger.error(f"Source directory {source_namespace_name} does not exist.")
        return

    if os.path.exists(new_namespace_path):
        logger.error(f"Target directory {new_namespace_name} already exists.")
        return

    shutil.copytree(source_namespace_path, new_namespace_path)
    logger.info(f"Copied {source_namespace_name} to {new_namespace_name}")
    return new_namespace_path


def replace_namespace_in_files(new_namespace_name, new_namespace_path):
    """Replace occurrences of the old namespace with the new one in all files."""
    sanitized_repo_name = sanitize_github_repository_name(new_namespace_name)

    for root, dirs, files in os.walk(new_namespace_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as file:
                file_content = file.read()

            # Replace all occurrences of the old namespace with the new one
            updated_content = re.sub(
                source_namespace_name, new_namespace_name, file_content
            )

            # Replace github_repository_name variable with the sanitized new name (without '-dev')
            updated_content = re.sub(
                r'github_repository_name\s*=\s*".*?"',
                f'github_repository_name = "{sanitized_repo_name}"',
                updated_content,
            )

            # Write the updated content back to the file
            with open(file_path, "w") as file:
                file.write(updated_content)

            logger.info(
                f"Updated {file_path} with new namespace: {new_namespace_name} and repository name: {sanitized_repo_name}"
            )


def commit_and_push_changes(new_namespace_name, branch_name):
    """Commit and push the new namespace directory to the repository."""
    logger.info(f"Committing changes for namespace {new_namespace_name}")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Add new namespace: {new_namespace_name}"],
        cwd=repo_dir,
        check=True,
    )
    subprocess.run(
        ["git", "push", "--set-upstream", "origin", branch_name],
        cwd=repo_dir,
        check=True,
    )
    logger.info(
        f"Pushed changes for namespace {new_namespace_name} to branch {branch_name}"
    )


def create_pull_request(branch_name, new_namespace_name):
    """Use the GitHub CLI to create a pull request."""
    pr_title = f"Add new namespace: {new_namespace_name}"
    pr_body = (
        f"This PR creates a new namespace for the application {new_namespace_name}."
    )
    subprocess.run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            pr_title,
            "--body",
            pr_body,
            "--base",
            "main",
            "--head",
            branch_name,
        ],
        cwd=repo_dir,
        check=True,
    )
    logger.info(f"Created pull request for branch {branch_name}")


def add_new_namespace(new_namespace_name):
    """Main function to add a new namespace by cloning, copying, replacing, and pushing."""
    clone_repo()
    branch_name = create_new_branch(new_namespace_name)
    new_namespace_path = copy_namespace_dir(new_namespace_name)
    if new_namespace_path:
        replace_namespace_in_files(new_namespace_name, new_namespace_path)
    commit_and_push_changes(new_namespace_name, branch_name)
    create_pull_request(branch_name, new_namespace_name)


def sanitize_github_repository_name(new_namespace_name):
    """Remove '-dev' suffix from the namespace name to form the GitHub repository name."""
    return new_namespace_name.replace("-dev", "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to add a new namespace in cloud-platform, replace namespace name, and create a PR"
    )
    parser.add_argument(
        "new_namespace_name", type=str, help="The name of the new namespace"
    )

    args = parser.parse_args()
    new_namespace_name = args.new_namespace_name

    add_new_namespace(new_namespace_name)
