"""
rename_project.py

This script automates the renaming process of a Flask template repository. 
It replaces all instances of a placeholder project name (like 'template-app-name') 
in filenames, directory names, and file contents with a new project name provided 
by the developer, **excluding** Markdown documentation files (.md). This is useful when 
starting a new project from a template, as it saves time and ensures consistency 
throughout the project, while keeping documentation unchanged.

How to Use:
1. Clone or copy the Flask template repository.
2. Run the script in a terminal using the following syntax:

   python rename_project.py <root_directory> <old_name> <new_name>
"""

import os
import sys


def replace_in_file(file_path, old_text, new_text):
    # Skip .md files
    if file_path.endswith(".md"):
        print(f"Skipping documentation file: {file_path}")
        return

    with open(file_path, "r") as file:
        content = file.read()

    new_content = content.replace(old_text, new_text)

    with open(file_path, "w") as file:
        file.write(new_content)


def rename_files_and_directories(root_dir, old_name, new_name):
    # Traverse through the directory
    for root, dirs, files in os.walk(root_dir):
        # Rename files
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Skip .md files for renaming
            if file_name.endswith(".md"):
                print(f"Skipping renaming for documentation file: {file_path}")
                continue

            if old_name in file_name:
                new_file_name = file_name.replace(old_name, new_name)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"Renamed file {file_path} to {new_file_path}")
            else:
                new_file_path = file_path

            # Replace placeholder text inside the file (skipping .md files)
            replace_in_file(new_file_path, old_name, new_name)

        # Rename directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if old_name in dir_name:
                new_dir_name = dir_name.replace(old_name, new_name)
                new_dir_path = os.path.join(root, new_dir_name)
                os.rename(dir_path, new_dir_path)
                print(f"Renamed directory {dir_path} to {new_dir_path}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python rename_project.py <root_directory> <old_name> <new_name>")
        sys.exit(1)

    root_directory = sys.argv[1]
    old_name = sys.argv[2]
    new_name = sys.argv[3]

    rename_files_and_directories(root_directory, old_name, new_name)
    print("Project renaming completed!")


if __name__ == "__main__":
    main()
