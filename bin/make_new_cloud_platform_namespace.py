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


def replace_namespace_in_files(
    new_namespace_name: str,
    new_namespace_path: str,
    repository_name: str,
    environment: str,
):
    """Replace occurrences of the old namespace with the new one in all files."""
    for root, _, files in os.walk(new_namespace_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as file:
                file_content = file.read()

            # Replace all occurrences of the old namespace with the new one
            updated_content = re.sub(
                source_namespace_name,
                new_namespace_name,
                file_content,
            )

            # Specifically update the github_repository_name Terraform variable block
            updated_content = re.sub(
                r'variable "github_repository_name" \{([^\}]*)default\s*=\s*".*?"',
                f'variable "github_repository_name" {{\\1default = "{repository_name}"',
                updated_content,
                flags=re.DOTALL,
            )

            # Replace occurrences of 'dev' with the selected environment (dev, staging, prod)
            updated_content = re.sub(
                r"\bdev\b",
                environment,
                updated_content,
            )

            # Write the updated content back to the file
            with open(file_path, "w") as file:
                file.write(updated_content)

            logger.info(
                f"Updated {file_path} with new namespace: {new_namespace_name} and repository name: {repository_name}"
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


def add_new_namespace(repository: str, environment: str):
    """Main function to add a new namespace by cloning, copying, replacing, and pushing."""
    clone_repo()
    new_namespace_name = f"{repository}-{environment}"
    branch_name = create_new_branch(new_namespace_name)
    new_namespace_path = copy_namespace_dir(new_namespace_name)
    if new_namespace_path:
        replace_namespace_in_files(
            new_namespace_name, new_namespace_path, repository, environment
        )
        run_terraform_fmt(new_namespace_path + "/resources")
    commit_and_push_changes(new_namespace_name, branch_name)
    create_pull_request(branch_name, new_namespace_name)
    clean_up_locally()


def run_terraform_fmt(new_namespace_path):
    """Run 'terraform fmt' to format the Terraform files in the new namespace directory."""
    logger.info(f"Running 'terraform fmt' on {new_namespace_path}")
    subprocess.run(["terraform", "fmt", new_namespace_path], check=True)
    logger.info(f"Formatted Terraform files in {new_namespace_path}")


def clean_up_locally():
    """Delete the cloud-platform-environments repository locally."""
    repo_dir = "./cloud-platform-environments"
    os.system(f"rm -rf {repo_dir}")


def sanitize_github_repository_name(new_namespace_name):
    """Remove '-dev' suffix from the namespace name to form the GitHub repository name."""
    return new_namespace_name.replace("-dev", "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add a new namespace to the cloud-platform-environments repository."
    )
    parser.add_argument("repository_name", type=str, help="The name of your repository")
    parser.add_argument(
        "environment",
        type=str,
        help="The environment type you want.",
        choices=["dev", "staging", "prod"],
    )

    args = parser.parse_args()

    add_new_namespace(args.repository_name, args.environment)
