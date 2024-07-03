#!/bin/bash

read -p "Increment Version? (s/N): " response

if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
  echo "Choose an option to increment the version:"
  echo "1) Major"
  echo "2) Minor"
  echo "3) Patch"
  echo "4) Pre-release"
  read -p "Enter your choice (1/2/3/4): " choice

  case $choice in
    1)
      poetry version major
      git add pyproject.toml
      git commit -m "chore: increase major version"
      echo "Incremented Major Version and pyproject.toml added for commit."
      ;;
    2)
      poetry version minor
      git add pyproject.toml
      git commit -m "chore: increase minor version"
      echo "Incremented Minor Version and pyproject.toml added for commit."
      ;;
    3)
      poetry version patch
      git add pyproject.toml
      git commit -m "chore: increase patch version"
      echo "Incremented Patch Version and pyproject.toml added for commit."
      ;;
    4)
      poetry version prerelease
      git add pyproject.toml
      git commit -m "chore: increase prerelease version"
      echo "Incremented Pre-release Version and pyproject.toml added for commit."
      ;;
    *)
      echo "Invalid choice. Version not incremented."
      ;;
  esac
else
  echo "Version not incremented."
fi
