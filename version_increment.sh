#!/bin/bash

# Use /dev/tty para garantir que a entrada seja lida do terminal
read -r -p "Increment Version? (s/N): " response </dev/tty



if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
  echo "Choose an option to increment the version:"
  echo "1) Major"
  echo "2) Minor"
  echo "3) Patch"
  read -r -p "Enter your choice (1/2/3): " choice </dev/tty

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
    *)
      echo "Invalid choice. Version not incremented."
      ;;
  esac
else
  echo "Version not incremented."
fi
