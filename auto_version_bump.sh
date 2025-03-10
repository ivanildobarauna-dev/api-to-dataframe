#!/usr/bin/env bash

set -e

# Function to display error messages and exit
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

# Check if pyproject.toml exists
if [[ ! -f pyproject.toml ]]; then
    error_exit "pyproject.toml not found in the current directory"
fi

# Check if git repo exists
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    error_exit "Not inside a git repository"
fi

echo "Checking if version needs to be bumped..."

# Function to extract version from pyproject.toml
get_version() {
    grep -E "^version\\s*=\\s*[\\"']" pyproject.toml | sed -E 's/version\\s*=\\s*["'\''](^["'\'']+)["'\''].*/\\1/'
}

# Check if pyproject.toml is staged
if git diff --name-only --cached | grep -q "pyproject.toml"; then
    echo "pyproject.toml is staged. Checking if version has been modified..."

    # Get the current version in the working copy
    current_version=$(get_version)

    # Get the version from the last commit
    previous_version=$(git show HEAD:pyproject.toml 2>/dev/null | grep -E "^version\\s*=\\s*[\\"']" | sed -E 's/version\\s*=\\s*["'\''](^["'\'']+)["'\''].*/\\1/' || echo "")

    if [[ "$current_version" != "$previous_version" ]]; then
        echo "Version has already been changed from $previous_version to $current_version. No need to bump version."
        exit 0
    fi
fi

# If we get here, we need to bump the version
echo "Bumping patch version..."
poetry version patch || error_exit "Failed to bump version with poetry"

new_version=$(get_version)
echo "Version bumped to $new_version"

# Stage the changes to pyproject.toml
git add pyproject.toml || error_exit "Failed to stage pyproject.toml"

echo "Successfully bumped version and staged pyproject.toml"
exit 0
